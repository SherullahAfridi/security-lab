from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models.feedback import Feedback


feedback = Blueprint("feedback", __name__)


@feedback.route("/feedback", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("All fields are required.", "danger")
            return redirect(url_for("feedback.index"))

        item = Feedback(
            name=name,
            email=email,
            message=message
        )

        db.session.add(item)
        db.session.commit()

        flash("Thank you for your feedback!", "success")

        return redirect(url_for("feedback.index"))

    return render_template("feedback.html")