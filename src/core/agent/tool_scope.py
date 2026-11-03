from extensions import AUTO_RUN_TOOLS

class ToolScope:
    """Which tools the LLM can use and which of those run without asking. A workflow limits use to what it declared; otherwise every tool is available."""

    def __init__(self, available=None, pre_approved=()):
        self.available = None if available is None else set(available)
        self.pre_approved = set(pre_approved)

    def is_available(self, tool_name):
        return self.available is None or tool_name in self.available

    def is_pre_approved(self, tool_name):
        return tool_name in AUTO_RUN_TOOLS or tool_name in self.pre_approved

    def filter(self, tool_schemas):
        return [schema for schema in tool_schemas if self.is_available(schema["function"]["name"])]
