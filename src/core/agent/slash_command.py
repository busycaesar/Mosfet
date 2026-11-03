from utils import get_skill_by_name, load_workflow
from .tool_scope import ToolScope

def parse_slash_command(user_input):
    if not user_input.startswith("/"):
        return None, ToolScope(), False

    parts = user_input[1:].split(maxsplit=1)

    if not parts:
        return None, ToolScope(), False

    name = parts[0]

    skill_content = get_skill_by_name(name)

    if skill_content is not None:
        return skill_content, ToolScope(), False

    workflow = load_workflow(name)

    if workflow is not None:
        content, approved_tools, declares_tools, declared_tools = workflow
        return content, ToolScope(available=declared_tools, pre_approved=approved_tools), declares_tools

    return None, ToolScope(), False
