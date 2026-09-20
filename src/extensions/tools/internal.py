from config import SKILLS_PATH
from utils import build_skill_file, update_skills_index, get_skill_by_name
from adapters import get_web_search
import trafilatura
from ..mcp import add_mcp_server, update_mcp_server

AUTO_RUN_TOOLS = set()

def auto_run(func):
    """Marks a tool as safe to run without asking the user for permission first."""
    AUTO_RUN_TOOLS.add(func.__name__)
    return func

def normalize_skill_name(name):
    return name.lower().replace(" ", "_")

def create_new_skill(name, description, content):
    if not name or not name.strip():
        return "Error: skill name must not be empty."
    if not description or not description.strip():
        return "Error: skill description must not be empty."
    if not content or not content.strip():
        return "Error: skill content must not be empty."

    name = normalize_skill_name(name)

    SKILLS_PATH.mkdir(parents=True, exist_ok=True)
    skill_path = SKILLS_PATH / f"{name}.md"

    with open(skill_path, "w") as file:
        skill_file_content = build_skill_file(description, content)
        file.write(skill_file_content)

@auto_run
def int_add_new_skill(name, description, content):
    error = create_new_skill(name, description, content)
    if error:
        return error

    update_skills_index(normalize_skill_name(name), description)

@auto_run
def int_get_skill_content(name):
    content = get_skill_by_name(name)

    if not content:
        return f"No skill available with name {name}."

    return content

@auto_run
def int_web_search_tool(query):
    return get_web_search().search(query)

def int_fetch_content_from_url(url):
    downloaded = trafilatura.fetch_url(url)

    if downloaded is None:
        return f"Could not fetch content from {url}."
    
    content = trafilatura.extract(downloaded)

    if not content:
        return f"No readable content found at {url}."

    return content

@auto_run
def int_add_mcp_server(name, url, command, args):
    try:
        available_tool_names = add_mcp_server(name, url=url, command=command, args=args)
    except Exception as error:
        return f"Could not add MCP server '{name}': {error}"
        
    return f"Added MCP server '{name}'. Discovered tools: {','.join(available_tool_names)}"

@auto_run
def int_update_mcp_server(name):
    try:
        available_tool_names = update_mcp_server(name)
    except Exception as error:
        return f"Could not update MCP server '{name}': {error}"

    return f"Updated MCP server '{name}'. Discovered tools: {','.join(available_tool_names)}"

def call_tool_function(name, args):
    if name == "int_add_new_skill":
        return int_add_new_skill(**args)
    elif name == "int_get_skill_content":
        return int_get_skill_content(**args)
    elif name == "int_web_search_tool":
        return int_web_search_tool(**args)
    elif name == "int_fetch_content_from_url":
        return int_fetch_content_from_url(**args)
    elif name == "int_add_mcp_server":
        return int_add_mcp_server(**args)
    elif name == "int_update_mcp_server":
        return int_update_mcp_server(**args)
    else:
        return f"No tool available with name {name}."