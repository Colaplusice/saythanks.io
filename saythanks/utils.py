# Email Infrastructure
# --------------------
from flask_mail import Message

from saythanks.extensions import mail

TEMPLATE = """{}

--{}

=========

This note of thanks was brought to you by SayThanks.io.

A Kenneth Reitz (me@kennethreitz.org) project.
"""


def send_notify(note):
    from flask import current_app

    # Say 'someone' if the byline is empty.
    who = note.byline or "someone"
    subject = "saythanks.io: {} sent a note!".format(who)
    body = TEMPLATE.format(note.body, note.byline)
    message = Message(
        sender=current_app.config["MAIL_SENDER"],
        recipients=[note.user.email],
        body=body,
        subject=subject,
    )
    mail.send(message)
