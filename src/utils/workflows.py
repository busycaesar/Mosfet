from config import WORKFLOWS_PATH, WORKFLOWS_INDEX_PATH
import json

def get_workflows_list():
    if not WORKFLOWS_INDEX_PATH.is_file():
        return {}

    content = WORKFLOWS_INDEX_PATH.read_text().strip()

    if not content:
        return {}

    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Workflows index at {WORKFLOWS_INDEX_PATH} is corrupted: {error}") from error

def get_workflow_by_name(name):
    workflow_path = WORKFLOWS_PATH / f"{name}.md"

    if not workflow_path.is_file():
        return None

    return workflow_path.read_text().strip()

def load_workflow(name):
    # Returns the workflow's steps plus those of every nested workflow (at any depth), and every tool approved for any of them; visited guards against cycles.
    if get_workflow_by_name(name) is None:
        return None

    index = get_workflows_list()
    sections, tools, visited, pending = [], [], set(), [name]

    while pending:
        current = pending.pop(0)

        if current in visited:
            continue

        visited.add(current)

        content = get_workflow_by_name(current)

        if content is None:
            continue

        sections.append(f'Workflow "{current}":\n{content}')

        entry = index.get(current, {})
        tools += entry.get("allowed_tools", []) + entry.get("allowed_mcp_tools", [])
        pending += entry.get("workflows", [])

    return "\n\n".join(sections), list(dict.fromkeys(tools))

def update_workflows_index(name, description, skills, workflows, tools, mcp_tools):
    index = get_workflows_list()
    index[name] = {
        "description": description,
        "skills": skills,
        "workflows": workflows,
        "tools": tools,
        "mcp_tools": mcp_tools,
        "allowed_tools": [],
        "allowed_mcp_tools": [],
    }

    WORKFLOWS_INDEX_PATH.write_text(json.dumps(index, indent=2))

def set_workflow_allowed_tools(name, allowed_tools, allowed_mcp_tools):
    index = get_workflows_list()

    if name in index:
        index[name]["allowed_tools"] = allowed_tools
        index[name]["allowed_mcp_tools"] = allowed_mcp_tools
        WORKFLOWS_INDEX_PATH.write_text(json.dumps(index, indent=2))
