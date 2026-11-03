import asyncio
from datetime import datetime, timezone
from utils import get_job_paths, get_workflow_by_name, load_job, save_job, delete_job, get_next_run
from .agent import invoke_agent, build_initial_messages
from .session import Session
from .unattended_activity_log import UnattendedActivityLog

CHECK_INTERVAL_SECONDS = 60

async def run_scheduler(channel, send_message):
    """Runs the channel's scheduled jobs as they come due. send_message(destination, text) is how the channel messages the user unprompted."""
    while True:
        for path in get_job_paths(channel):
            try:
                await _run_if_due(path, channel, send_message)
            except Exception as error:
                print(f"Warning: scheduled job {path} failed: {error}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

async def _run_if_due(path, channel, send_message):
    job = load_job(path)
    now = datetime.now(timezone.utc)

    if datetime.fromisoformat(job["next_run"]) > now:
        return

    # Running the prompt anyway would turn "/name" into ordinary chat with every tool offered.
    if get_workflow_by_name(job["workflow_name"]) is None:
        delete_job(path)
        await send_message(job["destination"], f"Cancelled the schedule for workflow '{job['workflow_name']}' because that workflow no longer exists.")
        return

    # Moved forward before running, so a run that outlasts the next check isn't started twice. Runs missed while offline happen once, not once per missed slot.
    job["next_run"] = get_next_run(job["schedule"], now).isoformat()
    save_job(path, job)

    await send_message(job["destination"], await _run_job(job, channel))

async def _run_job(job, channel):
    # A fresh conversation each run, never saved to disk; anything not pre-approved is denied, since nobody is there to approve it. It has no destination, so an unattended run can't schedule, list or cancel jobs; the result reaches the user through send_message.
    session = Session(channel, build_initial_messages(), path=None)

    try:
        return await asyncio.to_thread(invoke_agent, session, job["prompt"], _deny, UnattendedActivityLog())
    except Exception as error:
        return f"Scheduled workflow '{job['workflow_name']}' failed: {error}"

def _deny(function_name):
    return False
