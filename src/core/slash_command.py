from utils import get_skill_by_name, get_workflow_by_name

def get_slash_command_content(user_input):
    if not user_input.startswith("/"):
        return None

    parts = user_input[1:].split(maxsplit=1)

    if not parts:
        return None

    return get_skill_by_name(parts[0]) or get_workflow_by_name(parts[0])
