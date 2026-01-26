from rich.console import Console
from rich.text import Text
from InquirerPy import prompt
from .config import save_config

console = Console()


def show_big_branding():
    text = Text("""
 ██████╗ ███╗   ██╗██████╗ 
██╔════╝ ████╗  ██║██╔══██╗
██║  ███╗██╔██╗ ██║██████╔╝
██║   ██║██║╚██╗██║██╔═══╝ 
╚██████╔╝██║ ╚████║██║     
 ╚═════╝ ╚═╝  ╚═══╝╚═╝     

 Commit • Push • Done
""", style="bold cyan")
    console.print(text)


def init_command():
    show_big_branding()

    choice = prompt([
        {
            "type": "list",
            "name": "setup",
            "message": "Enable AI-generated commit messages?",
            "choices": [
                "🔑 Yes, provide API key",
                "⏭ Skip for now"
            ]
        }
    ])["setup"]

    config = {"llm": {}}

    if "provide" in choice.lower():
        api_key = prompt([
            {
                "type": "password",
                "name": "key",
                "message": "Paste your LLM API key:",
                "validate": lambda x: len(x.strip()) > 10
            }
        ])["key"]

        config["llm"] = {
            "enabled": True,
            "provider": "openai",
            "api_key": api_key
        }

        console.print("[bold green]✔ AI enabled[/bold green]")
    else:
        config["llm"] = {"enabled": False}
        console.print("[yellow]AI skipped[/yellow]")

    save_config(config)

    console.print("\n[bold green]Setup complete![/bold green]")
    console.print("[dim]Type `cnp` to commit and push[/dim]\n")


def config_command():
    show_big_branding()

    api_key = prompt([
        {
            "type": "password",
            "name": "key",
            "message": "Paste your LLM API key:",
            "validate": lambda x: len(x.strip()) > 10
        }
    ])["key"]

    save_config({
        "llm": {
            "enabled": True,
            "provider": "openai",
            "api_key": api_key
        }
    })

    console.print("[bold green]✔ API key saved[/bold green]")
