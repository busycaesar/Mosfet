from core import ActivityLog

class CLIActivityLog(ActivityLog):
    def __init__(self):
        self.ran_tool_calls = False

    def skill_injected(self, user_input):
        print(f"→ {user_input.split()[0]}: Loaded ")

    def tool_call_started(self, function_name, function_arguments):
        print(f"→ {function_name}({function_arguments}): Calling")

    def tool_call_finished(self, function_name):
        print(f"✓ {function_name} Done")

    def tool_batch_finished(self):
        print()
        self.ran_tool_calls = True

    def before_response(self):
        if not self.ran_tool_calls:
            print()
