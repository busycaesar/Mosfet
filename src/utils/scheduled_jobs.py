from config import SCHEDULE_PATH
from datetime import datetime, timezone
from croniter import croniter
import json

def create_job(channel, destination, workflow_name, workflow_input, schedule):
    now = datetime.now(timezone.utc)
    next_run = get_next_run(schedule, now)

    job = {
        "workflow_name": workflow_name,
        # Exactly what the user would type to run the workflow themselves.
        "prompt": f"/{workflow_name} {workflow_input or ''}".strip(),
        "schedule": schedule,
        "destination": destination,
        "next_run": next_run.isoformat(),
    }

    save_job(SCHEDULE_PATH / channel / f"{now.strftime('%Y%m%dT%H%M%S%fZ')}.json", job)

    return next_run

def get_job_paths(channel):
    return sorted((SCHEDULE_PATH / channel).glob("*.json"))

def load_job(path):
    return json.loads(path.read_text())

def save_job(path, job):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(job, indent=2))

def get_next_run(schedule, after):
    return croniter(schedule, after).get_next(datetime)
