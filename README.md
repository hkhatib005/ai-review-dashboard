# AI Code Review Bot + Dashboard

A GitHub Action that automatically reviews pull requests using the Claude API and posts inline comments. Includes a live web dashboard showing review history and stats, deployed on Render.

Code review is one of the highest-leverage activities in any engineering team, yet it is consistently the bottleneck that slows down shipping. This project automates the first pass — a GitHub Action that triggers on every pull request, analyzes the diff using the Claude API, and posts inline comments directly on the changed lines, just like a senior engineer would.

The architecture is intentionally lightweight: a Python script invoked by GitHub Actions reads the PR diff via the GitHub REST API, chunks it into reviewable segments, and sends each to Claude with a structured prompt tuned for code quality, security issues, and logic errors. The Flask dashboard provides a real-time view of all reviews, stats, and PR history.

## Tech Stack
- Python, Flask, Gunicorn
- Claude API (Anthropic)
- GitHub Actions
- Render (deployment)

## Features
- Auto-reviews every PR using Claude AI
- Posts inline comments per file changed
- Live dashboard with PR review stats
- One-click deploy to Render

## Deploy to Render
1. Fork this repo
2. Connect to Render as a Web Service
3. Add environment variables: `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, `REPO`
4. Deploy

## Environment Variables
```
GITHUB_TOKEN=your_github_token
ANTHROPIC_API_KEY=your_anthropic_key
REPO=owner/repo-to-review
```

## License
MIT