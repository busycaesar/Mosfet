def confirm_tool_call(function_name, function_arguments):
    answer = input(f"? Allow tool call {function_name}({function_arguments})? [Y/n]")
    return answer.strip().lower() == "y"
