import json
from .paths import CONFIG_PATH, CONFIG_FILE

# DEFAULTs
DEFAULT_LLM_PROVIDER = "OpenAI"
DEFAULT_WEB_SEARCH_PROVIDER = "DuckDuckGo"
DEFAULT_MODELS = {
    "OpenAI": "gpt-4o-mini",
    "Ollama": "qwen3:1.7b",
    "Anthropic": "claude-haiku-4-5",
}

# _read_config() is called from multiple places which re-reads and re-parses mosfet.config.json on every call.
# Instead we could declare the logic to get the value of config globally, but in that case the logic will be implemented everytime this file is imported, which makes it more expensive then calling the function multiple times whenever the value is needed.
def _read_config():
    config = {}

    if CONFIG_PATH.is_file():
        content = CONFIG_PATH.read_text().strip()

        if content:
            try:
                config = json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {CONFIG_FILE} isn't valid JSON. Using default values. Run 'mosfet config' to fix it.")

    return config

def get_llm_provider():
    return _read_config().get("LLM_PROVIDER") or DEFAULT_LLM_PROVIDER

def get_model():
    llm_provider = get_llm_provider()
    return _read_config().get("MODEL") or DEFAULT_MODELS.get(llm_provider, DEFAULT_MODELS[DEFAULT_LLM_PROVIDER])

def get_web_search_provider():
    return _read_config().get("WEB_SEARCH_PROVIDER") or DEFAULT_WEB_SEARCH_PROVIDER
