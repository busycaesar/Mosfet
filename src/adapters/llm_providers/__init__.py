from config import get_llm_provider, OLLAMA_BASE_URL, get_model, ANTHROPIC_MAX_TOKENS, ANTHROPIC_API_KEY, OPENAI_API_KEY
from .anthropic import AnthropicLLM
from .ollama import OllamaLLM
from .openai import OpenAILLM

def get_llm():
    # Choose the provider's class based on the provider and other configurations set in src/config/provider.py
    llm_provider = get_llm_provider()
    model = get_model()

    if llm_provider == "Anthropic":
        if not ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in .env before running Mosfet.")

        return AnthropicLLM(ANTHROPIC_API_KEY, model, ANTHROPIC_MAX_TOKENS)
    elif llm_provider == "Ollama":
        if not OLLAMA_BASE_URL:
            raise RuntimeError("OLLAMA_BASE_URL is not set for Ollama. Set it in /src/config/provider before running Mosfet.")

        return OllamaLLM(OLLAMA_BASE_URL, model)
    elif llm_provider == "OpenAI":
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set. Set it in .env before running Mosfet.")

        return OpenAILLM(OPENAI_API_KEY, model)
    else:
        raise RuntimeError(f"No adapter implemented yet for LLM_PROVIDER '{llm_provider}'.")
