import requests


def generate_commit_message(diff: str, api_key: str) -> str:
    """
    Send git diff to LLM and return a commit message.
    """

    if not diff.strip():
        return "chore: empty commit"

    prompt = f"""
You are a senior software engineer.

Given the following git diff, write a single concise,
clear git commit message.

Rules:
- Use present tense
- No markdown
- Max 72 characters
- No trailing punctuation

Git diff:
{diff}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You write excellent git commit messages."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 50,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    message = data["choices"][0]["message"]["content"].strip()

    # safety cleanup
    return message.split("\n")[0]
