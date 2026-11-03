from adapters import get_llm as get_raw_llm, ToolsNotSupported
from guardrails import GuardedLLM

def get_llm():
    return GuardedLLM(get_raw_llm())