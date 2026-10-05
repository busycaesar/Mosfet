from extensions import AUTO_RUN_TOOLS, call_tool_function
from utils import set_workflow_allowed_tools
import json

def run_tool_call(tool_call, confirm_tool_call, activity_log, allowed_tools):
    function_name = tool_call.function.name
    function_arguments = json.loads(tool_call.function.arguments)

    if not is_pre_approved(function_name, allowed_tools) and not confirm_tool_call(function_name.replace("int_", "")):
        return json.dumps("User denied permission to run this tool.")

    activity_log.tool_call_started(function_name, function_arguments)
    result = call_tool_function(function_name, function_arguments)
    activity_log.tool_call_finished(function_name)

    if function_name == "int_add_new_workflow" and isinstance(result, dict) and result.get("created"):
        approve_workflow_tools(result["workflow_name"], function_arguments, confirm_tool_call)

    return json.dumps(result)

def is_pre_approved(tool_name, allowed_tools=()):
    return tool_name in AUTO_RUN_TOOLS or tool_name in allowed_tools

def approve_workflow_tools(workflow_name, arguments, confirm_tool_call):
    # Asked once, right after the workflow is created, so it can later run (including unattended) without re-asking.
    approved_tools = [
        tool_name for tool_name in (arguments.get("tools") or [])
        if is_pre_approved(tool_name) or confirm_tool_call(f"{tool_name.replace('int_', '')} (needed by workflow '{workflow_name}')")
    ]

    approved_mcp_tools = [
        tool_name for tool_name in (arguments.get("mcp_tools") or [])
        if confirm_tool_call(f"{tool_name} (needed by workflow '{workflow_name}')")
    ]

    if approved_tools or approved_mcp_tools:
        set_workflow_allowed_tools(workflow_name, approved_tools, approved_mcp_tools)
