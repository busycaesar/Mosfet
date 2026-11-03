from config import WORKFLOWS_PATH, WORKFLOWS_INDEX_PATH
import json

def get_workflows_list():
    if not WORKFLOWS_INDEX_PATH.is_file():
        return {}

    content = WORKFLOWS_INDEX_PATH.read_text().strip()

    if not content:
        return {}

    try:
        index = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Workflows index at {WORKFLOWS_INDEX_PATH} is corrupted: {error}") from error

    # Workflows created before dependencies were tracked are stored as just their description.
    return {name: entry if isinstance(entry, dict) else {"description": entry} for name, entry in index.items()}

def get_workflow_by_name(name):
    workflow_path = WORKFLOWS_PATH / f"{name}.md"

    if not workflow_path.is_file():
        return None

    return workflow_path.read_text().strip()

def load_workflow(name):
    # Returns the steps of the workflow and every nested workflow (at any depth), every tool approved for any of them, whether any of them declares a tool or MCP tool, and the declared tools themselves, which are the only ones a workflow may use.
    if get_workflow_by_name(name) is None:
        return None

    sections, approved_tools, declared_tools = [], [], []

    for current, content, entry in _walk_workflows(name, get_workflows_list()):
        sections.append(f'Workflow "{current}":\n{content}')
        approved_tools += entry.get("allowed_tools", []) + entry.get("allowed_mcp_tools", [])
        declared_tools += entry.get("tools", []) + entry.get("mcp_tools", [])

    return "\n\n".join(sections), list(dict.fromkeys(approved_tools)), bool(declared_tools), list(dict.fromkeys(declared_tools))

def get_unapproved_tools(name):
    # Declared tools not approved yet, across the workflow and every nested workflow, each paired with the workflow that owns it.
    unapproved = []

    for current, _, entry in _walk_workflows(name, get_workflows_list()):
        for kind in ("tools", "mcp_tools"):
            allowed = entry.get(f"allowed_{kind}", [])
            unapproved += [{"workflow": current, "kind": kind, "tool": tool} for tool in entry.get(kind, []) if tool not in allowed]

    return unapproved

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

def add_workflow_allowed_tools(name, tools, mcp_tools):
    index = get_workflows_list()

    if name not in index:
        return

    entry = index[name]
    entry["allowed_tools"] = list(dict.fromkeys(entry.get("allowed_tools", []) + tools))
    entry["allowed_mcp_tools"] = list(dict.fromkeys(entry.get("allowed_mcp_tools", []) + mcp_tools))

    WORKFLOWS_INDEX_PATH.write_text(json.dumps(index, indent=2))

def _walk_workflows(name, index):
    # Yields the workflow and every nested workflow (at any depth) that still exists; visited guards against cycles.
    visited, pending = set(), [name]

    while pending:
        current = pending.pop(0)

        if current in visited:
            continue

        visited.add(current)

        content = get_workflow_by_name(current)

        if content is None:
            continue

        entry = index.get(current, {})

        yield current, content, entry

        pending += entry.get("workflows", [])
