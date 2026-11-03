from llm import get_llm, ToolsNotSupported
from .slash_command import parse_slash_command
from .tool_calls import run_tool_call
from .once_per_run_notice import OncePerRunNotice
from extensions import get_tools
from utils import clean_response
from config import TOOLS_UNSUPPORTED_CHAT_NOTICE, TOOLS_UNSUPPORTED_WORKFLOW_NOTICE

chat_notice = OncePerRunNotice(TOOLS_UNSUPPORTED_CHAT_NOTICE)

def invoke_agent(messages, user_input, confirm_tool_call, activity_log):
    original_length = len(messages)

    try:
        allowed_tools, requires_tools = build_context(messages, user_input, activity_log)

        try:
            response = agent_loop(messages, confirm_tool_call, activity_log, allowed_tools)

        except ToolsNotSupported:
            # A workflow that declares tools can't do its job without them, so a reply without tools would only pretend it ran.
            if requires_tools:
                del messages[original_length:]
                return TOOLS_UNSUPPORTED_WORKFLOW_NOTICE

            return _reply_without_tools(messages, activity_log)

    except Exception:
        del messages[original_length:]
        raise

    messages.append({"role": "assistant", "content": response})

    return response

def build_context(messages, user_input, activity_log):
    slash_command_content, allowed_tools, requires_tools = parse_slash_command(user_input)

    if slash_command_content is not None:
        messages.append({"role": "system", "content": slash_command_content})
        activity_log.skill_injected(user_input)

    messages.append({"role": "user", "content": user_input})

    return allowed_tools, requires_tools

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

def _reply_without_tools(messages, activity_log):
    llm_message = get_llm().infer(messages, [])

    activity_log.before_response()
    reply = clean_response(llm_message.content or "")

    # The notice is added after saving because it is for the user, not part of the conversation the model sees later.
    messages.append({"role": "assistant", "content": reply})

    return chat_notice.add_to(reply)
