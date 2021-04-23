import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskblog1 import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(
        current_app.root_path, "static", "profile_pics", picture_filename)

    output_size = (125, 125)
    resized_picture = Image.open(form_picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)

    previous_picture = os.path.join(
        current_app.root_path, "static", "profile_pics", current_user.image_file)
    if os.path.exists(previous_picture) and os.path.basename(previous_picture) != "default.jpg":
        os.remove(previous_picture)

    return picture_filename


def send_reset_email(user):
    token_url = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@flaskblog1.com",
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for("users.reset_token", token=token_url, _external=True)}

If you did not make this request, do not reply to this email - no changes will be made.
'''
    mail.send(msg)
