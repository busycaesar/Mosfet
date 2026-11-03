from abc import ABC, abstractmethod
import re
from .tools_not_supported import ToolsNotSupported

# The wording of the error is the only signal every provider has in common. It stays narrow because a false match would silently drop the tools from a request that could have used them.
TOOLS_NOT_SUPPORTED_PATTERN = re.compile(r"(does not|doesn't) support tools|tools? (is|are) not supported", re.IGNORECASE)

class LLMProvider(ABC):
    @abstractmethod
    def infer(self, messages, tools):
        """
        Send messages and the list of tools to the LLM to received the generated response or a tool to be called.
        """

    @abstractmethod
    def format_llm_response(self, generated_response):
        """
        Format the generated response by the model to append in the messages array.
        """

    @abstractmethod
    def format_tool_call_results(self, tool_call_results):
        """
        Format the result returned by the called tool into the messages array.
        """

    def _raise_if_tools_not_supported(self, error):
        """
        Turn a provider's tool-support rejection into ToolsNotSupported, so callers need not know each provider's error types. Any other error is left for the caller to handle.
        """
        if TOOLS_NOT_SUPPORTED_PATTERN.search(str(error)):
            raise ToolsNotSupported(str(error)) from error
