import time
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import ANSI
from rich.console import Console
from rich.markup import escape
from core import parse_user_input, build_initial_messages
from config import BANNER, WELCOME_MESSAGE, GOODBYE_MESSAGE
from .interaction import confirm_tool_call
from .activity_log import CLIActivityLog

console = Console()

PROMPT = ANSI("\033[1m\033[38;2;250;104;0m❯\033[0m ")
session = PromptSession(history=InMemoryHistory(), erase_when_done=True)

def run_cli_chat():
    messages = build_initial_messages()

    console.print(BANNER, style="bold #fa6800")
    console.print(WELCOME_MESSAGE)

    while True:
        try:
            console.print()
            user_input = session.prompt(PROMPT)
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n{GOODBYE_MESSAGE}")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        line_text = f"❯ {user_input}"
        padding = " " * max(0, console.width - len(line_text))
        console.print(f"[on #3a3a3a][bold #fa6800]❯[/bold #fa6800] {escape(user_input)}{padding}[/on #3a3a3a]")

        if user_input.lower() in ("exit", "quit"):
            console.print()
            console.print(GOODBYE_MESSAGE)
            break

        start_time = time.monotonic()

        console.print()

        try:
            with console.status("[dim]Biasing the gate...[/dim]", spinner="dots") as status:

                def confirm_tool_call_while_paused(function_name):
                    status.stop()
                    try:
                        return confirm_tool_call(function_name)
                    finally:
                        status.start()

                activity_log = CLIActivityLog()
                response = parse_user_input(messages, user_input, confirm_tool_call_while_paused, activity_log)
        except Exception as error:
            console.print(f"[red]Error:[/red] {escape(str(error))}. Please try again.")
            continue

        elapsed = time.monotonic() - start_time

        console.print(f"[bold #fa6800]●[/bold #fa6800] {escape(response)}")
        console.print(f"[dim]✻ Threshold reached in {elapsed:.0f}s[/dim]")
