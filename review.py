import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]

def get_pr_diff(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()

def review_diff(diff_text):
    headers = {
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": f"Review this code diff and give concise, actionable feedback:\n\n{diff_text}"}]
    }
    r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
    return r.json()["content"][0]["text"]

def post_comment(repo, pr_number, body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    requests.post(url, headers=headers, json={"body": body})

if __name__ == "__main__":
    repo = os.environ.get("REPO", "owner/repo")
    pr_number = int(os.environ.get("PR_NUMBER", "1"))
    files = get_pr_diff(repo, pr_number)
    for f in files[:3]:
        diff = f.get("patch", "")
        if diff:
            feedback = review_diff(diff)
            post_comment(repo, pr_number, f"**AI Review - {f['filename']}**\n\n{feedback}")
    print("Review complete.")
