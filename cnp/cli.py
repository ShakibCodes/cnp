import sys
from rich.console import Console
from rich.panel import Panel
from InquirerPy import prompt

from .git_ops import run_command, capture
from .init import init_command, config_command
from .config import load_config
from .llm import generate_commit_message


console = Console()


def main():
    # command routing
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_command()
            return
        if sys.argv[1] == "-m" and len(sys.argv) > 2 and sys.argv[2] == "config":
            config_command()
            return

    # normal cnp flow
    console.print(
        Panel.fit(
            "[bold cyan]CNP[/bold cyan]\n[dim]Commit and Push[/dim]",
            border_style="cyan"
        )
    )

    with console.status("[bold green]Running git add .[/bold green]"):
        run_command(["git", "add", "."])

    diff = capture(["git", "diff", "--staged"])
    config = load_config()
    llm_enabled = config and config.get("llm", {}).get("enabled", False)

    if llm_enabled:
        api_key = config["llm"]["api_key"]

        try:
            with console.status("[bold cyan]Generating commit message with AI...[/bold cyan]"):
                message = generate_commit_message(diff, api_key)

            console.print(f"\n[bold]AI commit message:[/bold] {message}\n")

            use_ai = prompt([
                {
                    "type": "confirm",
                    "name": "ok",
                    "message": "Use this commit message?",
                    "default": True
                }
            ])["ok"]

            if not use_ai:
                raise Exception("User rejected AI message")

        except Exception:
            message = prompt([
                {
                    "type": "input",
                    "name": "msg",
                    "message": "Enter commit message manually:",
                    "validate": lambda x: len(x.strip()) > 0
                }
            ])["msg"]

    else:
        while True:
            message = prompt([
                {
                    "type": "input",
                    "name": "msg",
                    "message": "Enter your commit message:",
                    "validate": lambda x: len(x.strip()) > 0
                }
            ])["msg"]

            confirm = prompt([
                {
                    "type": "confirm",
                    "name": "ok",
                    "message": "Confirm commit message?",
                    "default": True
                }
            ])["ok"]

            if confirm:
                break


    run_command(["git", "commit", "-m", message])

    branch = capture(["git", "branch", "--show-current"])

    with console.status(f"[bold cyan]Pushing to origin/{branch}...[/bold cyan]"):
        run_command(["git", "push", "-u", "origin", branch])

    console.print("[bold green]✔ Done![/bold green]")


if __name__ == "__main__":
    main()
