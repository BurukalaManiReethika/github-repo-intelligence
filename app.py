from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    repo = None
    error = None

    if request.method == "POST":

        repo_url = request.form["repo_url"]

        try:
            parts = repo_url.rstrip("/").split("/")
            owner = parts[-2]
            repo_name = parts[-1]

            repo_api = f"https://api.github.com/repos/{owner}/{repo_name}"
            lang_api = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
            contrib_api = f"https://api.github.com/repos/{owner}/{repo_name}/contributors"
            readme_api = f"https://api.github.com/repos/{owner}/{repo_name}/readme"

            repo_res = requests.get(repo_api)

            if repo_res.status_code != 200:
                raise Exception()

            data = repo_res.json()

            languages = requests.get(lang_api).json()

            contributors = requests.get(contrib_api).json()

            readme = requests.get(readme_api)

            readme_text = ""

            if readme.status_code == 200:

                encoded = readme.json()["content"]

                readme_text = base64.b64decode(encoded).decode(
                    "utf-8",
                    errors="ignore"
                )[:1000]

            health = 50

            if data["stargazers_count"] > 50:
                health += 15

            if data["forks_count"] > 20:
                health += 10

            if data["open_issues_count"] < 10:
                health += 10

            if data["watchers_count"] > 20:
                health += 10

            if data["description"]:
                health += 5

            if health > 100:
                health = 100

            repo = {
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
                "url": data["html_url"],
                "health": health,
                "languages": languages,
                "contributors": contributors[:5],
                "readme": readme_text
            }

        except:
            error = "Invalid GitHub Repository"

    return render_template(
        "index.html",
        repo=repo,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
