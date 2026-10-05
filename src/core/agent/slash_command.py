from utils import get_skill_by_name, load_workflow

def parse_slash_command(user_input):
    if not user_input.startswith("/"):
        return None, []

    parts = user_input[1:].split(maxsplit=1)

    if not parts:
        return None, []

    name = parts[0]

    skill_content = get_skill_by_name(name)

    if skill_content is not None:
        return skill_content, []

    workflow = load_workflow(name)

    if workflow is not None:
        return workflow

    return None, []
