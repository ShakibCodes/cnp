import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Command failed:", " ".join(command))
        print("Return code:", e.returncode)
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
    except subprocess.CalledProcessError as e:
        print("Command failed:", " ".join(command))
        print(e.stderr)
        sys.exit(1)

def main():
    print("Running cnp (Commit and Push)")
    
    run_command(["git", "add", "."])

    status = capture(["git", "status", "--porcelain"])
    if not status:
        print("Nothing to commit.")
        sys.exit(0)

    while True:
        message = input("Enter your commit message: ").strip()

        if not message:
            print("Commit message cannot be empty")
            continue

        print(f"Commit message: {message}")
        confirm = input("Confirm commit message (y/n): ").strip().lower()

        if confirm in ("y", "yes"):
            break
        elif confirm in ("n", "no"):
            print("Re-enter commit message\n")
        else:
            print("Please enter 'y' or 'n'\n")

    run_command(["git", "commit", "-m", message])

    branch = capture(["git", "branch", "--show-current"])

    run_command(["git", "push", "-u", "origin", branch])

    print("Done!")

if __name__ == "__main__":
    main()
