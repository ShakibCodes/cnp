import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Command failed:", " ".join(command))
        sys.exit(1);

def capture(command):
    try:
        result = subprocess.run(
            command, 
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Command failed:", " ".join(command))
        sys.exit(1);


def main():
    print("Running cnp (Commit and Push)")
    run_command(["git", "add", "."])
    
    ab = capture(["git", "diff", "--staged"]) # this is dummy and currently Experimental
 

    while(True):
        message = input("Enter your commit message: ").strip()

        if not message:
            print("Commit message cannot be empty")
            continue
        print(f"Commit message: {message}") 

        confirm = input("Confirm commit message(y/n): ").lower()
        if confirm=="y":
            break;
        elif confirm=='n':
            print("Re-enter commit message")
        else:
            print("Please enter 'y' or 'n'\n")



    run_command(["git", "commit", "-m", message])


    detect_branch = capture(["git", "branch", "--show-current"])

    run_command(["git", "push", "-u", "origin", detect_branch])

    print("Done!")
    
if __name__ == "__main__":
    main()