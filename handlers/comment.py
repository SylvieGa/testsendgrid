from flask import render_template, request, redirect, url_for, Blueprint

from models.settings import db
from models.topic import Topic
from models.user import User
from models.comments import Comment
from utils.email_helper import send_email

from utils.redis_helper import create_csrf_token, validate_csrf

comment_handlers = Blueprint("comment", __name__)

@comment_handlers.route("/topic/<topic_id>/create-comment", methods=["POST"])
    def comment_create(topic_id):
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for('auth.login'))
    
    csrf = request.form.get("csrf")

    if validate_csrf(csrf, user.username):
        text = request.form.get("text")
        topic = db.query(Topic).get(int(topic_id))
        comment = Comment.create(topic=topic, text=text, author=user)

        return redirect(url_for('topic.topic_details', topic_id=topic_id, csrf_token=create_csrf_token(user.username)))

    else:
        return "CSRF Token ist not valid"
    
    @classmethod
def create(cls, text, author, topic):
    comment = cls(text=text, author=author, topic=topic)
    db.add(comment)
    db.commit()

    # only send of topic author has her/his email in the database
    if topic.author.email_address:
        send_email(receiver_email=topic.author.email_address, subject="New comment for your topic!",
                   text="Your topic {} has a new comment.".format(topic.title))

    return comment
