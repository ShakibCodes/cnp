# Git cnp (Commit and Push)

A streamlined Python CLI tool to automate the standard `git add`, `git commit`, and `git push` workflow.

## Features

* **Auto-Staging**: Automatically runs `git add .` to stage all changes.
* **Change Detection**: Checks for local changes before asking for a message. If the working tree is clean, it exits gracefully.
* **Safety Confirmation**: Displays your commit message and asks for confirmation (`y/n`) to ensure no typos make it into your history.
* **Branch Awareness**: Automatically detects your current active branch and pushes to `origin`.
* **Error Handling**: Built-in checks to stop execution if a Git command fails, providing the return code and error details.