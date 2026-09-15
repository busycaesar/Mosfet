import questionary

def confirm_tool_call(function_name):
    answer = questionary.select(
        f"Allow tool call {function_name}",
        choices=["Yes", "No"],
    ).ask()

    return answer == "Yes"
