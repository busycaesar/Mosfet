import json
from datetime import datetime, timezone
from config import SESSIONS_PATH, get_llm_provider
from .build_initial_message import build_initial_messages

SESSION_FILE_SUFFIX = ".jsonl"
CORRUPT_FILE_SUFFIX = ".corrupt"

def start_session(channel):
    channel_path = SESSIONS_PATH / channel
    latest_path = _find_latest_session_file(channel_path)

    if latest_path is not None:
        session = _load_session(channel, latest_path)

        if session is not None:
            return session

    return Session(channel, build_initial_messages(), _build_new_session_path(channel_path))

class Session:
    """
    One conversation for one channel. Only the messages added after the initial system messages are stored on disk.
    """
    
    def __init__(self, channel, messages, path, resumed=False):
        self.channel = channel
        self.messages = messages
        self.path = path
        self.resumed = resumed

    def _build_header(self):
        return {
            "type": "session",
            "channel": self.channel,
            "provider": get_llm_provider(),
            "created": datetime.now(timezone.utc).isoformat(),
        }
    
    def save_turn(self, start_index):
        new_messages = self.messages[start_index:]

        if not new_messages:
            return

        try:
            # Serialize everything before touching the file so a failure can never leave half a turn on disk.
            lines = [json.dumps(to_jsonable(message), ensure_ascii=False) for message in new_messages]

            if not self.path.exists():
                self.path.parent.mkdir(parents=True, exist_ok=True)
                lines.insert(0, json.dumps(self._build_header()))

            with open(self.path, "a", encoding="utf-8") as file:
                file.write("\n".join(lines) + "\n")
        except (OSError, TypeError, ValueError) as error:
            print(f"Warning: could not save the conversation to {self.path}: {error}")
    
def to_jsonable(value):
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]

    # LLM SDKs put their own objects (pydantic models) in the history, e.g. OpenAI's message or Anthropic's content blocks.
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)

    return value

def _find_latest_session_file(channel_path):
    if not channel_path.is_dir():
        return None

    # File names are UTC timestamps, so the last one alphabetically is the newest.
    session_files = sorted(channel_path.glob(f"*{SESSION_FILE_SUFFIX}"))

    return session_files[-1] if session_files else None

def _build_new_session_path(channel_path):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

    return channel_path / f"{timestamp}{SESSION_FILE_SUFFIX}"

def _load_session(channel, path):
    try:
        header, saved_messages = _parse_session_file(path)
    except (OSError, ValueError) as error:
        print(f"Warning: the saved {channel} conversation at {path} is unreadable ({error}). Setting it aside and starting a new conversation.")
        _set_aside(path)
        return None

    saved_provider = header.get("provider")
    current_provider = get_llm_provider()

    # Message formats differ between providers, so a history saved under one can't be replayed to another.
    if saved_provider != current_provider:
        print(f"Warning: the previous {channel} conversation was saved with {saved_provider}, but the provider is now {current_provider}. Starting a new conversation; the old one is kept on disk.")
        return None

    # The initial system messages are rebuilt so the available-skills list is current.
    return Session(channel, build_initial_messages() + saved_messages, path, resumed=True)

def _parse_session_file(path):
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if not lines:
        raise ValueError("the file is empty")

    header = json.loads(lines[0])

    if not isinstance(header, dict) or header.get("type") != "session":
        raise ValueError("the session header is missing")

    saved_messages = []

    for index, line in enumerate(lines[1:], start=1):
        try:
            message = json.loads(line)
        except json.JSONDecodeError as error:
            # A bad last line is just a write that was cut short (e.g. a crash), so drop it instead of failing.
            if index == len(lines) - 1:
                break
            raise ValueError(f"line {index + 1} is not valid JSON") from error

        if not isinstance(message, dict) or "role" not in message:
            raise ValueError(f"line {index + 1} is not a message")

        saved_messages.append(message)

    return header, saved_messages

def _set_aside(path):
    try:
        path.rename(path.with_name(path.name + CORRUPT_FILE_SUFFIX))
    except OSError:
        pass
