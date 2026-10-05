from llm import get_llm
from .slash_command import parse_slash_command
from .tool_calls import run_tool_call
from extensions import get_tools
from utils import clean_response

def invoke_agent(messages, user_input, confirm_tool_call, activity_log):
    original_length = len(messages)

    try:
        allowed_tools = build_context(messages, user_input, activity_log)
        
        response = agent_loop(messages, confirm_tool_call, activity_log, allowed_tools)

    except Exception:
        del messages[original_length:]
        raise

    messages.append({"role": "assistant", "content": response})

    return response

def build_context(messages, user_input, activity_log):
    slash_command_content, allowed_tools = parse_slash_command(user_input)

    if slash_command_content is not None:
        messages.append({"role": "system", "content": slash_command_content})
        activity_log.skill_injected(user_input)

    messages.append({"role": "user", "content": user_input})

    return allowed_tools

def agent_loop(messages, confirm_tool_call, activity_log, allowed_tools):
    llm = get_llm()

    while True:
        llm_message = llm.infer(messages, get_tools())

        if not llm_message.tool_calls:
            activity_log.before_response()
            return clean_response(llm_message.content or "")

        messages.append(llm.format_llm_response(llm_message))

        tool_call_results = [
            (tool_call.id, run_tool_call(tool_call, confirm_tool_call, activity_log, allowed_tools))
            for tool_call in llm_message.tool_calls
        ]

        activity_log.tool_batch_finished()

        messages.extend(llm.format_tool_call_results(tool_call_results))
