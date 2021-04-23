from flask import render_template, request, Blueprint
from flaskblog1.models import Post

main = Blueprint("main", __name__)


@ main.route("/")
@ main.route("/home")
def home():
    # name = request.args.get("name", "Home Page")
    # return f"<h1> {escape(name)} </h1>"
    page_queried = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page_queried, per_page=5)
    return render_template("home.html", posts=posts)


@ main.route("/about")
def about():
    # name = request.args.get("name", "About Page")
    # return f"<h1> {escape(name)} </h1>"
    return render_template("about.html", title="About")
