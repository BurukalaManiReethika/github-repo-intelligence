from flask import Flask, render_template, request, jsonify
import requests
import base64
import json
import os

app = Flask(__name__)

@app.template_filter("format_number")
def format_number(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

GITHUB_API = "https://api.github.com"

# Use a token from env if available to avoid rate limits
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def calculate_score(repo):
    score = 50
    if repo["stargazers_count"] > 50:
        score += 10
    if repo["forks_count"] > 20:
        score += 10
    if repo["watchers_count"] > 20:
        score += 10
    if repo["description"]:
        score += 5
    if repo["license"]:
        score += 5
    if len(repo.get("topics", [])) > 0:
        score += 5
    if repo["open_issues_count"] < 10:
        score += 5
    return min(score, 100)


def parse_owner_repo(url):
    """Extract owner and repo name from a GitHub URL."""
    parts = url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid URL")
    return parts[-2], parts[-1]


# ── Simple in-memory favorites store (persists per process) ─────────────────
# In production you'd swap this for a database.
_favorites = {}   # keyed by repo_url


@app.route("/favorite", methods=["POST"])
def favorite():
    data = request.get_json(silent=True) or request.form
    repo_url  = data.get("repo_url", "").strip()
    repo_name = data.get("repo_name", "")
    stars     = data.get("stars", 0)
    language  = data.get("language", "")

    if not repo_url:
        return jsonify({"status": "error", "message": "repo_url required"}), 400

    if repo_url in _favorites:
        # Toggle: remove if already favorited
        del _favorites[repo_url]
        return jsonify({"status": "removed"})

    _favorites[repo_url] = {
        "repo_name": repo_name,
        "repo_url":  repo_url,
        "stars":     stars,
        "language":  language,
    }
    return jsonify({"status": "saved"})


@app.route("/favorites")
def favorites():
    return render_template("favorites.html", favorites=list(_favorites.values()))


@app.route("/", methods=["GET", "POST"])
def home():
    repo  = None
    error = None

    if request.method == "POST":
        url = request.form.get("repo_url", "").strip()
        try:
            owner, repository = parse_owner_repo(url)
            headers = get_headers()

            # ── Core repo data ───────────────────────────────────────────────
            repo_res = requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}",
                headers=headers,
                timeout=10,
            )
            if repo_res.status_code != 200:
                raise ValueError("Repository not found")
            repo_data = repo_res.json()

            # ── Languages ────────────────────────────────────────────────────
            lang_res = requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/languages",
                headers=headers,
                timeout=10,
            )
            languages = lang_res.json() if lang_res.status_code == 200 else {}

            # ── Contributors ─────────────────────────────────────────────────
            contrib_res = requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/contributors",
                headers=headers,
                timeout=10,
            )
            contributors = contrib_res.json()[:6] if contrib_res.status_code == 200 else []

            # ── README ───────────────────────────────────────────────────────
            readme_res = requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/readme",
                headers=headers,
                timeout=10,
            )
            readme_text = ""
            if readme_res.status_code == 200:
                readme_text = base64.b64decode(
                    readme_res.json()["content"]
                ).decode("utf-8", errors="ignore")[:3000]

            repo = {
                "name":         repo_data["name"],
                "owner":        repo_data["owner"]["login"],
                "avatar":       repo_data["owner"]["avatar_url"],
                "description":  repo_data.get("description") or "No description provided.",
                "stars":        repo_data["stargazers_count"],
                "forks":        repo_data["forks_count"],
                "watchers":     repo_data["watchers_count"],
                "issues":       repo_data["open_issues_count"],
                "language":     repo_data.get("language") or "N/A",
                "created":      repo_data["created_at"][:10],
                "updated":      repo_data["updated_at"][:10],
                "url":          repo_data["html_url"],
                "license":      repo_data["license"]["name"] if repo_data.get("license") else "No License",
                "topics":       repo_data.get("topics", []),
                "languages":    languages,
                "contributors": contributors,
                "readme":       readme_text,
                "health":       calculate_score(repo_data),
                "is_favorite":  repo_data["html_url"] in _favorites,
            }

            return render_template("dashboard.html", repo=repo)

        except ValueError as e:
            error = str(e) or "Invalid GitHub Repository URL"
        except Exception:
            error = "Could not fetch repository. Check the URL and try again."

    return render_template("index.html", repo=None, error=error)


if __name__ == "__main__":
    app.run(debug=True)
