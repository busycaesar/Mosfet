from .base import LLMProvider
from openai import BadRequestError, OpenAI, omit

class OllamaLLM(LLMProvider):
    def __init__(self, base_url, model):
        self.model = model
        # Using the OpenAI SDK for Ollama because it is compatible and also saves us a lot of time by not writing the translation logic.
        # Local server ignores the key, but the SDK requires a non-empty string.
        self.client = OpenAI(api_key="ollama", base_url=base_url)

    def infer(self, messages, tools):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools or omit
            )
        except BadRequestError as error:
            self._raise_if_tools_not_supported(error)
            raise

        return completion.choices[0].message

    def format_llm_response(self, generated_response):
        return generated_response

    def format_tool_call_results(self, tool_call_results):
        return [
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": result
            }
            for tool_call_id, result in tool_call_results
        ]
