import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "development-only-secret"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///security_lab.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.posts import posts
    app.register_blueprint(posts)

    from app.routes.feedback import feedback
    app.register_blueprint(feedback)

    @app.route("/")
    def home():
        return render_template("home.html")

    with app.app_context():
        from app.models.user import User
        db.create_all()

    return app