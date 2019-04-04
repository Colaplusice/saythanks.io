from peewee import *
from playhouse.shortcuts import model_to_dict

from .utils import send_notify
from .extensions import db


class User(db.Model):
    nickname = CharField(null=False, unique=True)
    email = CharField(null=False)
    profile = CharField(null=True)
    password = CharField(null=False)
    avatar = CharField(null=True)
    is_enabled = BooleanField(default=True)
    is_email_enabled = BooleanField(default=True)

    @classmethod
    def disable_email(cls, nickname):
        cls.update(email_enabled=False).where(cls.nickname == nickname).execute()

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.select().where(cls.nickname == nickname).first()

    @classmethod
    def enable_email(cls, nickname):
        cls.update(email_enabled=True).where(cls.nickname == nickname).execute()

    @classmethod
    def disable_account(cls, nickname):
        cls.update(is_enabled=False).where(cls.nickname == nickname).execute()

    @classmethod
    def enable_account(cls, nickname):
        cls.update(is_enabled=True).where(cls.nickname == nickname).execute()


class Note(db.Model):
    body = CharField()
    user = ForeignKeyField(User, User.nickname)
    byline = CharField()
    archived = BooleanField(default=False)

    @classmethod
    def get_archived_notes(cls, nickname):
        notes = cls.select().where(cls.user == nickname, cls.archived == True)
        return [model_to_dict(note, recurse=False) for note in notes]

    @classmethod
    def get_unarchive_by_user(cls, nickname):
        notes = cls.select().where(cls.user == nickname, cls.archived == False)
        return [model_to_dict(note, recurse=False) for note in notes]

    def notify(self):
        send_notify(self)
