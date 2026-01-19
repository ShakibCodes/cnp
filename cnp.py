import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Command failed:", " ".join(command))
        sys.exit(1);


def main():
    print("Running cnp (Commit and Push)")
    run_command(["git", "add", "."])

    message = input("Enter your commit message: ").strip()


    if not message:
        print("Commit message cannot be empty")
        sys.exit(1)

    run_command(["git", "commit", "-m", message])

    run_command(["git", "push", "-u", "origin", "main"])

    print("Done!")

if __name__ == "__main__":
    main()