import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from InquirerPy import prompt

console = Console()


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        console.print(
            f"[bold red]Command failed:[/bold red] {' '.join(command)}"
        )
        sys.exit(1)


def capture(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        console.print(
            f"[bold red]Command failed:[/bold red] {' '.join(command)}"
        )
        sys.exit(1)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]CNP[/bold cyan]\n[dim]Commit and Push[/dim]",
            border_style="cyan"
        )
    )

    with console.status("[bold green]Running git add .[/bold green]"):
        run_command(["git", "add", "."])

    # unchanged (still experimental / unused)
    ab = capture(["git", "diff", "--staged"])

    while True:
        message = prompt([
            {
                "type": "input",
                "name": "msg",
                "message": "Enter your commit message:",
                "validate": lambda x: len(x.strip()) > 0
            }
        ])["msg"].strip()

        console.print(f"\n[bold]Commit message:[/bold] {message}\n")

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
        else:
            console.print("[yellow]Re-enter commit message[/yellow]\n")

    with console.status("[bold cyan]Creating commit...[/bold cyan]"):
        run_command(["git", "commit", "-m", message])

    detect_branch = capture(["git", "branch", "--show-current"])

    with console.status(
        f"[bold cyan]Pushing to origin/{detect_branch}...[/bold cyan]"
    ):
        run_command(["git", "push", "-u", "origin", detect_branch])

    console.print("[bold green]✔ Done![/bold green]")


if __name__ == "__main__":
    main()