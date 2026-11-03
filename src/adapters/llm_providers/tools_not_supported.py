class ToolsNotSupported(Exception):
    """
    Raised when a provider rejects a request because the model does not support tools.
    """
