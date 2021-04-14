import os
import secrets
from PIL import Image
from flask import Flask, render_template, escape, request, url_for, flash, redirect, request, abort
from flaskblog1 import app, db, bcrypt
from flaskblog1.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog1.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@ app.route("/")
@ app.route("/home")
def home():
    # name = request.args.get("name", "Home Page")
    # return f"<h1> {escape(name)} </h1>"
    page_queried = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page_queried, per_page=5)
    return render_template("home.html", posts=posts)


@ app.route("/about")
def about():
    # name = request.args.get("name", "About Page")
    # return f"<h1> {escape(name)} </h1>"
    return render_template("about.html", title="About")


@ app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account for {form.username.data} created, you can now log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Registration", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"User {form.email.data} logged in successfully", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(
                f"Email {form.email.data} not found or password is incorrect", "danger")
    return render_template("login.html", title="Login", form=form)


@ app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(
        app.root_path, "static", "profile_pics", picture_filename)

    output_size = (125, 125)
    resized_picture = Image.open(form_picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)

    previous_picture = os.path.join(
        app.root_path, "static", "profile_pics", current_user.image_file)
    if os.path.exists(previous_picture) and os.path.basename(previous_picture) != "default.jpg":
        os.remove(previous_picture)

    return picture_filename


@ app.route("/account", methods=["GET", "POST"])
@ login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/create/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been added!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))


@ app.route("/user/<string:username>")
def user_posts(username):
    page_queried = request.args.get("page", 1, type=int)
    user_queried = User.query.filter_by(username=username).first_or_404()
    posts = (Post.query.filter_by(author=user_queried)
             .order_by(Post.date_posted.desc())
             .paginate(page=page_queried, per_page=5))
    return render_template("user_posts.html", posts=posts, user=user_queried)


@ app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
    return render_template("reset_request.html", title="Reset Password", form=form)


@ app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Token invalid", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    return render_template("reset_token.html", title="Reset Password", form=form")
