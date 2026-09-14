from .tools import tool_schemas, call_tool_function as call_internal_tool_function, AUTO_RUN_TOOLS
from .mcp import get_mcp_tools, is_mcp_tool as mcp_has_tool, call_tool_function as call_mcp_tool_function

def get_tools():
    return tool_schemas + get_mcp_tools()

def call_tool_function(name, args):
    if mcp_has_tool(name):
        return call_mcp_tool_function(name, args)
    return call_internal_tool_function(name, args)