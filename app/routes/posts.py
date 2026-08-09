from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models.post import Post, Comment

posts = Blueprint("posts", __name__)


@posts.route("/posts")
def index():
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/index.html", posts=all_posts)


@posts.route("/posts/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            return "Title and content are required.", 400

        post = Post(title=title, content=content)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("posts.index"))

    return render_template("posts/create.html")


@posts.route("/posts/<int:post_id>")
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail.html", post=post)


@posts.route("/posts/<int:post_id>/comment", methods=["POST"])
def comment(post_id):
    post = Post.query.get_or_404(post_id)

    content = request.form.get("content", "").strip()

    if not content:
        return "Comment cannot be empty.", 400

    comment = Comment(
        content=content,
        post=post
    )

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for("posts.detail", post_id=post.id))