import copy
from config import messages
from utils import get_skills_list

def build_initial_messages():
    initial_messages = copy.deepcopy(messages)
    available_skills = get_skills_list()

    if available_skills:
        initial_messages.append({
            "role": "system",
            "content": f"You have the following skills available. When a skill fits the request, use the tool that loads a skill's full instructions by name, then follow them:\n{available_skills}."
        })

    return initial_messages
