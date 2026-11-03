from .activity_log import ActivityLog

class UnattendedActivityLog(ActivityLog):
    """Nobody is watching an unattended run (e.g. a scheduled job), so tool activity only goes to the process log."""

    def skill_injected(self, user_input):
        pass

    def tool_call_started(self, function_name, function_arguments):
        print(f"[unattended] {function_name}({function_arguments})")

    def tool_call_finished(self, function_name):
        pass

    def tool_batch_finished(self):
        pass

    def before_response(self):
        pass
