from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

GITHUB_API = "https://api.github.com"


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

    if len(repo["topics"]) > 0:
        score += 5

    if repo["open_issues_count"] < 10:
        score += 5

    return min(score,100)
    @app.route("/favorite", methods=["POST"])
def favorite():

    repo_name = request.form["repo_name"]

    repo_url = request.form["repo_url"]

    stars = request.form["stars"]

    language = request.form["language"]

    exists = FavoriteRepository.query.filter_by(
        repo_url=repo_url
    ).first()
    @app.route("/favorites")
    def favorites():

    favorites = FavoriteRepository.query.all()

    return render_template(
        "favorites.html",
        favorites=favorites
    )

    if exists:
        return {"status": "exists"}

    favorite = FavoriteRepository(
        repo_name=repo_name,
        repo_url=repo_url,
        stars=stars,
        language=language
    )

    db.session.add(favorite)
    db.session.commit()

    return {"status": "saved"}

history = SearchHistory(

    repo_name=repo["name"],

    repo_url=repo["url"]

)

db.session.add(history)

db.session.commit()
@app.route("/",methods=["GET","POST"])
def home():

    repo=None
    error=None

    if request.method=="POST":

        url=request.form["repo_url"]

        try:

            owner=url.rstrip("/").split("/")[-2]
            repository=url.rstrip("/").split("/")[-1]

            headers={
                "Accept":"application/vnd.github+json"
            }

            repo_res=requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}",
                headers=headers
            )

            if repo_res.status_code!=200:
                raise Exception()

            repo_data=repo_res.json()

            language=requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/languages"
            ).json()

            contributors=requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/contributors"
            ).json()

            readme=requests.get(
                f"{GITHUB_API}/repos/{owner}/{repository}/readme"
            )

            readme_text=""

            if readme.status_code==200:

                readme_text=base64.b64decode(

                    readme.json()["content"]

                ).decode(

                    "utf-8",
                    errors="ignore"

                )[:3000]

            repo={

                "name":repo_data["name"],

                "owner":repo_data["owner"]["login"],

                "avatar":repo_data["owner"]["avatar_url"],

                "description":repo_data["description"],

                "stars":repo_data["stargazers_count"],

                "forks":repo_data["forks_count"],

                "watchers":repo_data["watchers_count"],

                "issues":repo_data["open_issues_count"],

                "language":repo_data["language"],

                "created":repo_data["created_at"][:10],

                "updated":repo_data["updated_at"][:10],

                "url":repo_data["html_url"],

                "license":repo_data["license"]["name"] if repo_data["license"] else "No License",

                "topics":repo_data.get("topics",[]),

                "languages":language,

                "contributors":contributors[:6],

                "readme":readme_text,

                "health":calculate_score(repo_data)

            }

            return render_template(

                "dashboard.html",

                repo=repo

            )

        except Exception:

            error="Invalid GitHub Repository URL"

    return render_template(

        "index.html",

        repo=None,

        error=error

    )


if __name__=="__main__":

    app.run(debug=True)
