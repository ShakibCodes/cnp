import sys
from rich.console import Console
from rich.panel import Panel
from InquirerPy import prompt

from .git_ops import run_command, capture
from .init import init_command, config_command

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

    capture(["git", "diff", "--staged"])

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
