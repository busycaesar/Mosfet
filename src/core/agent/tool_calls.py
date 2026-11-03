from extensions import call_tool_function
import json

def run_tool_call(tool_call, context, activity_log, tool_scope):
    function_name = tool_call.function.name
    function_arguments = json.loads(tool_call.function.arguments)

    if not tool_scope.is_available(function_name):
        return json.dumps(f"'{function_name}' isn't available here: a workflow can only use the tools it declared.")

    if not tool_scope.is_pre_approved(function_name) and not context.confirm_tool_call(function_name.replace("int_", "")):
        return json.dumps("User denied permission to run this tool.")

    activity_log.tool_call_started(function_name, function_arguments)
    result = call_tool_function(function_name, function_arguments, context)
    activity_log.tool_call_finished(function_name)

    return json.dumps(result)
