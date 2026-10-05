from config import SKILLS_PATH, SKILLS_INDEX_PATH
import json

def get_skills_list():
    if not SKILLS_INDEX_PATH.is_file():
        return {}

    content = SKILLS_INDEX_PATH.read_text().strip()

    if not content:
        return {}

    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Skills index at {SKILLS_INDEX_PATH} is corrupted: {error}") from error

def get_skill_by_name(name):
    skill_path = SKILLS_PATH / f"{name}.md"

    if not skill_path.is_file():
        return None

    return skill_path.read_text().strip()

def update_skills_index(name, description):
    index = get_skills_list()
    index[name] = description

    SKILLS_INDEX_PATH.write_text(json.dumps(index, indent=2))
