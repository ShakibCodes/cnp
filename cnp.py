import subprocess
import sys
import argparse
from typing import List


class CommandError(RuntimeError):
    """Custom exception for command failures."""


def run(command: List[str], capture_output=False) -> str:
    """Run a command safely."""
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=capture_output,
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        raise CommandError(
            f"\n❌ Command failed: {' '.join(command)}"
            f"\nReturn code: {e.returncode}"
            f"\n{e.stderr or ''}"
        ) from e


def git(*args, capture_output=False) -> str:
    """Run a git command."""
    return run(["git", *args], capture_output=capture_output)


def has_changes() -> bool:
    """Check if there are staged or unstaged changes."""
    status = git("status", "--porcelain", capture_output=True)
    return bool(status.strip())


def get_branch() -> str:
    """Get current branch name."""
    return git("branch", "--show-current", capture_output=True)


def confirm(prompt: str) -> bool:
    """Ask for yes/no confirmation."""
    while True:
        choice = input(f"{prompt} [y/n]: ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_commit_message(auto: bool) -> str:
    """Prompt or auto-generate commit message."""
    if auto:
        return "chore: automated commit"

    while True:
        message = input("Enter commit message: ").strip()
        if not message:
            print("⚠ Commit message cannot be empty.")
            continue

        print(f"\nMessage: {message}")
        if confirm("Use this message?"):
            return message


def ensure_git_repo():
    """Verify current directory is a git repo."""
    try:
        git("rev-parse", "--is-inside-work-tree")
    except CommandError:
        print("❌ Not a git repository.")
        sys.exit(1)


def ensure_remote_exists():
    """Ensure origin remote exists."""
    remotes = git("remote", capture_output=True)
    if "origin" not in remotes.split():
        print("❌ No 'origin' remote found.")
        sys.exit(1)


def push(branch: str, dry_run: bool):
    """Push branch with upstream setup."""
    if dry_run:
        print(f"[DRY RUN] git push -u origin {branch}")
        return

    try:
        git("push", "-u", "origin", branch)
    except CommandError:
        print("⚠ Push failed. Trying without upstream...")
        git("push", "origin", branch)


def main():
    parser = argparse.ArgumentParser(description="Commit & Push helper")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing")
    parser.add_argument("--auto", action="store_true", help="Auto commit message")
    args = parser.parse_args()

    try:
        print("🚀 Running CNP (Commit & Push)\n")

        ensure_git_repo()
        ensure_remote_exists()

        if args.dry_run:
            print("[DRY RUN MODE ENABLED]\n")

        if not args.dry_run:
            git("add", ".")

        if not has_changes():
            print("✔ Nothing to commit.")
            return

        message = get_commit_message(args.auto)

        branch = get_branch()
        print(f"📌 Branch: {branch}")

        if args.dry_run:
            print(f"[DRY RUN] git commit -m \"{message}\"")
        else:
            git("commit", "-m", message)

        push(branch, args.dry_run)

        print("\n✅ Done!")

    except KeyboardInterrupt:
        print("\n⚠ Aborted by user.")
        sys.exit(130)
    except CommandError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()