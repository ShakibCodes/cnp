import subprocess
import sys
from rich.console import Console

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
