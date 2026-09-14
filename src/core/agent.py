from llm import get_llm
from .slash_command import get_skill_content
from .agent_log import log_skill_injection, log_llm_call, log_tool_call
from extensions import get_tools, call_tool_function, AUTO_RUN_TOOLS
import json
from utils import clean_response

def parse_user_input(messages, user_input, confirm_tool_call):
    original_length = len(messages)

    try:
        skill_content = get_skill_content(user_input)

        if skill_content is not None:
            messages.append({"role": "system", "content": skill_content})
            log_skill_injection(user_input)

        messages.append({"role": "user", "content": user_input})

        response = agent_loop(messages, confirm_tool_call)
       
    except Exception:
        del messages[original_length:]
        raise

    messages.append({"role": "assistant", "content": response})

    return response
    
def agent_loop(messages, confirm_tool_call):
    llm = get_llm()

    while True:
        llm_message = llm.infer(messages, get_tools())
        
        if not llm_message.tool_calls:
            content = llm_message.content or ""
            response = clean_response(content)
            break

        messages.append(llm.format_llm_response(llm_message))

        tool_call_results = []

        for tool_call in llm_message.tool_calls:
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments)

            run_permission = True if function_name in AUTO_RUN_TOOLS else False

            if not run_permission:
                permission = confirm_tool_call(function_name, function_arguments)

                if not permission: 
                    result = "User denied permission to run this tool."
                    tool_call_results.append((tool_call.id, result))
                    continue

            log_llm_call(function_name, function_arguments)
            result = call_tool_function(function_name, function_arguments)
            log_tool_call(function_name)

            tool_call_results.append((tool_call.id, json.dumps(result)))

        messages.extend(llm.format_tool_call_results(tool_call_results))
    
    return response