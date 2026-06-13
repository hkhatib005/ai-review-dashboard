import os
import requests
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("REPO", "hkhatib005/ai-code-review-bot")

def github_headers():
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def get_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls"
    r = requests.get(url, headers=github_headers(), params={"state": "all", "per_page": 20})
    return r.json() if r.ok else []

def get_pr_comments(pr_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    r = requests.get(url, headers=github_headers())
    comments = r.json() if r.ok else []
    return [c for c in comments if "AI Review" in c.get("body", "")]

def get_repo_stats():
    url = f"https://api.github.com/repos/{REPO}"
    r = requests.get(url, headers=github_headers())
    return r.json() if r.ok else {}

@app.route("/")
def index():
    return render_template("index.html", repo=REPO)

@app.route("/api/stats")
def stats():
    prs = get_pull_requests()
    stats = get_repo_stats()
    total_prs = len(prs)
    reviewed_prs = 0
    total_comments = 0
    recent_reviews = []
    for pr in prs:
        comments = get_pr_comments(pr["number"])
        if comments:
            reviewed_prs += 1
            total_comments += len(comments)
            recent_reviews.append({"pr_number": pr["number"], "title": pr["title"], "author": pr["user"]["login"], "state": pr["state"], "comments": len(comments), "url": pr["html_url"], "created_at": pr["created_at"][:10]})
    return jsonify({"total_prs": total_prs, "reviewed_prs": reviewed_prs, "total_comments": total_comments, "stars": stats.get("stargazers_count", 0), "recent_reviews": recent_reviews[:10]})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "repo": REPO, "timestamp": datetime.utcnow().isoformat()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
