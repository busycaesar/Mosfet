from config import SCHEDULE_PATH
from datetime import datetime, timezone
from croniter import croniter
import json

# Exactly what the schedule tool promises the model. croniter also accepts seconds and year fields, but the scheduler only checks once a minute.
CRON_FIELD_COUNT = 5

def is_valid_schedule(schedule):
    return len(schedule.split()) == CRON_FIELD_COUNT and croniter.is_valid(schedule)

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

def get_jobs(channel, destination):
    jobs = []

    for path in get_job_paths(channel):
        try:
            job = load_job(path)
        except ValueError as error:
            print(f"Warning: skipping unreadable scheduled job {path}: {error}")
            continue

        if job.get("destination") == destination:
            jobs.append({"job_id": path.stem, **job})

    return jobs

def cancel_job(channel, destination, job_id):
    # The id comes from the model, so it must match one of this destination's own jobs before it is used in a path.
    if not any(job["job_id"] == job_id for job in get_jobs(channel, destination)):
        return False

    delete_job(SCHEDULE_PATH / channel / f"{job_id}.json")

    return True

def load_job(path):
    return json.loads(path.read_text())

def save_job(path, job):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(job, indent=2))

def delete_job(path):
    path.unlink(missing_ok=True)

def get_next_run(schedule, after):
    return croniter(schedule, after).get_next(datetime)
