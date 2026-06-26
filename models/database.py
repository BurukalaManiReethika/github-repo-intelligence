from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class SearchHistory(db.Model):

    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)

    repo_name = db.Column(db.String(200), nullable=False)

    repo_url = db.Column(db.String(500), nullable=False)

    searched_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class FavoriteRepository(db.Model):

    __tablename__ = "favorite_repository"

    id = db.Column(db.Integer, primary_key=True)

    repo_name = db.Column(db.String(200))

    repo_url = db.Column(db.String(500))

    stars = db.Column(db.Integer)

    language = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
