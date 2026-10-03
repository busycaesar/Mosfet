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

def update_workflows_index(name, description):
    index = get_workflows_list()
    index[name] = description

    WORKFLOWS_INDEX_PATH.write_text(json.dumps(index, indent=2))
