from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from werkzeug.security import generate_password_hash

from app import db
from app.models.user import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. You can now log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash(
                "Both email and password are required.",
                "danger"
            )
            return redirect(url_for("auth.login"))

        user = User.query.filter(
            User.email == email
        ).first()

        if not user or not user.check_password(password):
            flash(
                "Invalid email or password.",
                "danger"
            )
            return redirect(url_for("auth.login"))

        # Store logged-in user's ID in the session
        session["user_id"] = user.id
        session["username"] = user.username

        flash("Login successful.", "success")

        return redirect(url_for("home"))

    return render_template("login.html")


@auth.route("/logout")
def logout():

    # Remove login information from the session
    session.pop("user_id", None)
    session.pop("username", None)

    flash("You have been logged out.", "success")

    return redirect(url_for("home"))