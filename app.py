from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    repo_data = None
    error = None

    if request.method == "POST":
        repo_url = request.form.get("repo_url")

        try:
            parts = repo_url.rstrip("/").split("/")
            owner = parts[-2]
            repo = parts[-1]

            api = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api)

            if response.status_code == 200:
                data = response.json()

                repo_data = {
                    "name": data["name"],
                    "owner": data["owner"]["login"],
                    "description": data["description"],
                    "stars": data["stargazers_count"],
                    "forks": data["forks_count"],
                    "watchers": data["watchers_count"],
                    "issues": data["open_issues_count"],
                    "language": data["language"],
                    "created": data["created_at"][:10],
                    "updated": data["updated_at"][:10],
                    "url": data["html_url"]
                }

            else:
                error = "Repository not found."

        except Exception:
            error = "Invalid GitHub URL."

    return render_template(
        "index.html",
        repo=repo_data,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
