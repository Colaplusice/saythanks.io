# -*- coding: utf-8 -*-

#  _____         _____ _           _
# |   __|___ _ _|_   _| |_ ___ ___| |_ ___
# |__   | .'| | | | | |   | .'|   | '_|_ -|
# |_____|__,|_  | |_| |_|_|__,|_|_|_,_|___|
#           |___|

import os
from functools import wraps

from flask import Flask, request, session, render_template, url_for,g
from flask import abort, redirect, Markup, make_response
from flask_common import Common
from names import get_full_name

from .extensions import db, mail, babel
from .models import Note, User

# from raven.contrib.flask import Sentry

# Application Basics
# ------------------

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")


class Config:
    DATABASE_URL = "postgresql://localhost/say_thanks"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    LANGUAGES = ['en', 'zh']
    # note: in debug mode when app created, this variable
    # will reload from .env. but production mode will not
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_SENDER = os.environ.get("MAIL_SENDER")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")


class ProductionConfig(Config):
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_URL = "postgresql://{user}:{password}@db/say_thanks".format(
        user=DATABASE_USER, password=DATABASE_PASSWORD
    )


print("test env: ", os.environ.get("MAIL_SENDER"))

if app.env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(Config)
res = mail.init_app(app)
# Flask-Common.
common = Common(app)

# Sentry for catching application errors in production.
# if "SENTRY_DSN" in os.environ:
#     sentry = Sentry(app, dsn=os.environ["SENTRY_DSN"])
auth_callback_url = "locahost:5000/callback"

# DATABASE
db.init_app(app)

# db.database.create_tables([User, Note])


# babel
# app.config.from_pyfile('babel.cfg')
babel.init_app(app)


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "nickname" not in session:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated


# Application Routes
# ------------------


@app.route("/")
def index():
    return render_template("index.html", callback_url=auth_callback_url)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form = request.form
        User.get_or_create(**form)
        return redirect(url_for(".index"))
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        if User.get_by_nickname(nickname) is not None:
            session["nickname"] = nickname
            return redirect(url_for(".inbox"))
    return render_template("login.html")


@app.route("/inbox")
@requires_auth
def inbox():
    # Auth0 stored account information.
    nickname = session["nickname"]
    user = User.get_by_nickname(nickname)
    user_notes = Note.get_unarchive_by_user(nickname)
    # Grab the inbox from the database.
    is_enabled = user.is_enabled
    is_email_enabled = user.is_email_enabled
    # Send over the list of all given notes for the user.
    return render_template(
        "inbox.html",
        user=user,
        notes=user_notes,
        is_enabled=is_enabled,
        is_email_enabled=is_email_enabled,
    )


@app.route("/inbox/export/<format>")
@requires_auth
def inbox_export(format):
    # Auth0 stored account information.
    nickname = session["nickname"]
    # Grab the inbox from the database.
    user = User.get_by_nickname(nickname)
    # inbox = Inbox.select().where(Inbox.user == nickname).first()
    # Send over the list of all given notes for the user.
    response = make_response(inbox.export(format))
    response.headers["Content-Disposition"] = "attachment; filename=saythanks-inbox.csv"
    response.headers["Content-type"] = "text/csv"
    return response


@app.route("/inbox/archived")
@requires_auth
def archived_inbox():
    # Auth0 stored account information.
    # Grab the inbox from the database.
    user = User.get_by_nickname(session["nickname"])
    archived_notes = Note.get_archived_notes(session["nickname"])
    is_enabled = user.is_enabled
    is_email_enabled = user.is_email_enabled
    # Send over the list of all given notes for the user.
    return render_template(
        "inbox_archived.html",
        user=user,
        notes=archived_notes,
        inbox=inbox,
        is_enabled=is_enabled,
        is_email_enabled=is_email_enabled,
    )


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", callback_url=auth_callback_url)


@app.route("/disable-email")
@requires_auth
def disable_email():
    # Auth0 stored account information.
    User.disable_email(session["nickname"])
    return redirect(url_for("inbox"))


@app.route("/enable-email")
@requires_auth
def enable_email():
    # Auth0 stored account information.
    User.enable_email(session["nickname"])
    return redirect(url_for("inbox"))


@app.route("/disable-inbox")
@requires_auth
def disable_inbox():
    # Auth0 stored account information.
    User.disable_account(session["nickname"])
    return redirect(url_for("inbox"))


@app.route("/enable-inbox")
@requires_auth
def enable_inbox():
    # Auth0 stored account information.
    User.enable_account(session["nickname"])
    return redirect(url_for("inbox"))


@app.route("/to/<nickname>", methods=["GET"])
def display_submit_note(nickname):
    user = User.get_by_nickname(nickname)
    if not user:
        abort(404)
    if not user.is_enabled:
        abort(404)
    fake_name = get_full_name()
    return render_template("submit_note.html", user=user, fake_name=fake_name)


@app.route("/note/<uuid>", methods=["GET"])
def share_note(uuid):
    # Abort if the note is not found.
    note = Note.get_by_id(uuid)
    return render_template("share_note.html", note=note)


@app.route("/inbox/archive/note/<uuid>", methods=["GET"])
@requires_auth
def archive_note(uuid):
    # Auth0 stored account information.
    note = Note.get_by_id(uuid)
    # Archive the note.
    note.archived = True
    note.save()
    # Redirect to the archived inbox.
    return redirect(url_for("inbox"))


@app.route("/to/<nickname>/submit", methods=["POST"])
def submit_note(nickname):
    # Fetch the current inbox.
    user = User.get_by_nickname(nickname)
    # Replace newlines with <br> tags.
    body = request.form["body"]
    body = "---NEWLINE---".join(body.split("\n"))
    # Strip any HTML away.
    body = Markup(body).striptags()
    byline = Markup(request.form["byline"]).striptags()
    # Crazy hack to get br tags preserved.
    body = "<br>".join(body.split("---NEWLINE---"))
    # Assert that the body has length.
    if not body:
        # Pretend that it was successful.
        return redirect(url_for("thanks"))

    # Store the incoming note to the database.
    note = Note.create(body=body, byline=byline, user=user.nickname)
    # Email the user the new note.
    if user.is_email_enabled:
        note.notify()
    return redirect(url_for("thanks"))


@app.route("/callback")
def callback_handling():
    nickname = request.args.get("nickname")
    session["nickname"] = nickname
    User.get_or_create()
    return redirect(url_for("inbox"))
