from config import SKILLS_PATH, WORKFLOWS_PATH
from utils import build_content_file, update_skills_index, get_skill_by_name, update_workflows_index, get_workflow_by_name, get_unapproved_tools, add_workflow_allowed_tools, is_valid_schedule, create_job, get_jobs, cancel_job
from adapters import get_web_search
import trafilatura
from ..mcp import add_mcp_server, update_mcp_server

AUTO_RUN_TOOLS = set()

def auto_run(func):
    """Marks a tool as safe to run without asking the user for permission first."""
    AUTO_RUN_TOOLS.add(func.__name__)
    return func

def normalize_name(name):
    return name.lower().replace(" ", "_")

def create_new_skill(name, description, content):
    if not name or not name.strip():
        return "Error: skill name must not be empty."
    if not description or not description.strip():
        return "Error: skill description must not be empty."
    if not content or not content.strip():
        return "Error: skill content must not be empty."

    name = normalize_name(name)

    if get_workflow_by_name(name) is not None:
        return _name_taken_error("workflow", name)

    SKILLS_PATH.mkdir(parents=True, exist_ok=True)
    skill_path = SKILLS_PATH / f"{name}.md"

    with open(skill_path, "w") as file:
        skill_file_content = build_content_file(description, content)
        file.write(skill_file_content)

@auto_run
def int_add_new_skill(name, description, content):
    error = create_new_skill(name, description, content)

    if error:
        return error

    update_skills_index(normalize_name(name), description)

@auto_run
def int_get_skill_content(name):
    content = get_skill_by_name(name)

    if not content:
        return f"No skill available with name {name}."

    return content

def create_new_workflow(name, description, content):
    if not name or not name.strip():
        return "Error: workflow name must not be empty."
    if not description or not description.strip():
        return "Error: workflow description must not be empty."
    if not content or not content.strip():
        return "Error: workflow content must not be empty."

    name = normalize_name(name)

    if get_skill_by_name(name) is not None:
        return _name_taken_error("skill", name)

    WORKFLOWS_PATH.mkdir(parents=True, exist_ok=True)
    workflow_path = WORKFLOWS_PATH / f"{name}.md"

    with open(workflow_path, "w") as file:
        workflow_file_content = build_content_file(description, content)
        file.write(workflow_file_content)

@auto_run
def int_add_new_workflow(
        name, 
        description, 
        content, 
        skills, 
        workflows,
        tools,
        mcp_tools,
        context
    ):

    error = create_new_workflow(name, description, content)

    if error:
        return error

    normalized_name = normalize_name(name)

    # Not every provider enforces the schema, so a model can send null for "none".
    tools, mcp_tools = tools or [], mcp_tools or []

    update_workflows_index(normalized_name, description, skills, workflows, tools, mcp_tools)

    # Asked once, right now, so the workflow can later run (including on a schedule) without asking again.
    approved_tools = [tool for tool in tools if tool in AUTO_RUN_TOOLS or context.confirm_tool_call(_needed_by(tool, normalized_name))]
    approved_mcp_tools = [tool for tool in mcp_tools if context.confirm_tool_call(_needed_by(tool, normalized_name))]

    add_workflow_allowed_tools(normalized_name, approved_tools, approved_mcp_tools)

    return f"Created workflow '{normalized_name}'."

@auto_run
def int_schedule_job(workflow_name, workflow_input, schedule, context):
    workflow_name = normalize_name(workflow_name)

    if get_workflow_by_name(workflow_name) is None:
        return f"Not scheduled: there is no workflow named '{workflow_name}'."

    # A skill wins over a workflow of the same name when "/name" runs, so the job would never run this workflow.
    if get_skill_by_name(workflow_name) is not None:
        return f"Not scheduled: a skill is also named '{workflow_name}' and would run instead of the workflow."

    if not is_valid_schedule(schedule):
        return f"Not scheduled: '{schedule}' is not a valid 5-field cron expression."

    session = context.session

    if session.destination is None:
        return "Not scheduled: this channel has nowhere to send a scheduled workflow's results."

    # Scheduled runs can't ask for approval, so every tool the workflow (or a nested one) declared must be approved now, all or nothing.
    unapproved = [item for item in get_unapproved_tools(workflow_name) if item["tool"] not in AUTO_RUN_TOOLS]

    if unapproved:
        tool_names = ", ".join(dict.fromkeys(item["tool"].replace("int_", "") for item in unapproved))

        if not context.confirm_tool_call(f"{tool_names} (needed to run workflow '{workflow_name}' on a schedule)"):
            return f"Not scheduled: scheduled runs can't ask for approval, so these tools must all be approved first: {tool_names}."

        _save_approvals(unapproved)

    next_run = create_job(session.channel, session.destination, workflow_name, workflow_input, schedule)

    return f"Scheduled workflow '{workflow_name}' ({schedule}, UTC). Next run: {next_run.strftime('%Y-%m-%d %H:%M')} UTC."

@auto_run
def int_list_scheduled_jobs(context):
    session = context.session
    jobs = get_jobs(session.channel, session.destination)

    if not jobs:
        return "No scheduled jobs in this conversation."

    return jobs

@auto_run
def int_cancel_scheduled_job(job_id, context):
    session = context.session

    if not cancel_job(session.channel, session.destination, job_id):
        return f"Not cancelled: this conversation has no scheduled job with id '{job_id}'."

    return f"Cancelled scheduled job '{job_id}'."

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

def call_tool_function(name, args, context):
    if name == "int_add_new_skill":
        return int_add_new_skill(**args)
    elif name == "int_get_skill_content":
        return int_get_skill_content(**args)
    elif name == "int_add_new_workflow":
        return int_add_new_workflow(**args, context=context)
    elif name == "int_schedule_job":
        return int_schedule_job(**args, context=context)
    elif name == "int_list_scheduled_jobs":
        return int_list_scheduled_jobs(context=context)
    elif name == "int_cancel_scheduled_job":
        return int_cancel_scheduled_job(**args, context=context)
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

def _name_taken_error(other_kind, name):
    return f"Error: a {other_kind} named '{name}' already exists. Skills and workflows can't share a name because /{name} would only run one of them."

def _needed_by(tool_name, workflow_name):
    return f"{tool_name.replace('int_', '')} (needed by workflow '{workflow_name}')"

def _save_approvals(unapproved):
    for item in unapproved:
        is_mcp_tool = item["kind"] == "mcp_tools"
        add_workflow_allowed_tools(item["workflow"], [] if is_mcp_tool else [item["tool"]], [item["tool"]] if is_mcp_tool else [])
