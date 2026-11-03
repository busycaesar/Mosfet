class ToolContext:
    """What a tool may need beyond its own arguments: the session the request came from, and a way to ask the user for permission."""

    def __init__(self, session, confirm_tool_call):
        self.session = session
        self.confirm_tool_call = confirm_tool_call
