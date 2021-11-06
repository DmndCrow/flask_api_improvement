from enum import unique
from . import db


class Person(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    sort_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    image = db.Column(db.String(100))
    nationality = db.Column(db.String(10), server_default='GB')

    email = db.Column(db.String(100), unique=True)
    twitter = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    wikidata = db.Column(db.String(20))


class Organization(db.Model):
    group_id = db.Column(db.String(70), primary_key=True)
    group = db.Column(db.String(100))

    wikidata_group = db.Column(db.String(20))


class Membership(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    group_id = db.Column(db.String(70), primary_key=True)
