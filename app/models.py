from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


"""
class NewFeed(db.Model):
    __tablename__ = "NewFeed"
    feedTitle = db.Column(db.String(80))
    feedDescription = db.Column(db.String(255))
    feedURL = db.Column(db.String(255), primary_key=True, unique = True)
    feedCategory = db.Column(db.String(255))

    def __init__(self, feedTitle, feedURL, feedCategory, feedDescription):
        self.feedTitle = feedTitle;
        self.feedURL = feedURL;
        self.feedCategory = feedCategory;
        self.feedDescription = feedDescription;

"""


class Feed(db.Model):
    __tablename__ = "Feed"
    feedTitle = db.Column(db.String(80))
    feedDescription = db.Column(db.String(255))
    feedURL = db.Column(db.String(255), primary_key=True, unique = True)
    feedCategory = db.Column(db.String(255))
    feedModified = db.Column(db.String(35))
    feedEtag = db.Column(db.String, nullable=True)
    FeedEntries = db.relationship('FeedEntry', backref='Feed',
                                lazy='dynamic')
    FeedEntriesTest = db.relationship('FeedEntryTest', backref='Feed',
                                lazy='dynamic')

    def __init__(self, feedTitle, feedURL, feedCategory, feedDescription, feedModified, feedEtag):
        self.feedTitle = feedTitle;
        self.feedURL = feedURL;
        self.feedCategory = feedCategory;
        self.feedModified = feedModified;
        self.feedDescription = feedDescription;
        self.feedEtag = feedEtag;


class FeedEntry(db.Model):
    __tablename__ = "FeedEntry"
    id = db.Column(db.Integer(), primary_key=True)
    EntryTitle = db.Column(db.String(80))
    EntrySummary = db.Column(db.String(200))
    EntryURL = db.Column(db.String(255))
    EntryDate = db.Column(db.DateTime(255))
    feed_url = db.Column(db.String, db.ForeignKey('Feed.feedURL'))

    def __init__(self, EntryTitle, EntrySummary, EntryURL, EntryDate):
        self.EntryTitle = EntryTitle;
        self.EntrySummary = EntrySummary;
        self.EntryURL = EntryURL;
        self.EntryDate = EntryDate;

class FeedEntryTest(db.Model):
    __tablename__ = "FeedEntryTest"
    id = db.Column(db.Integer(), primary_key=True)
    TestEntryTitle = db.Column(db.String(80))
    TestEntrySummary = db.Column(db.String(200))
    TestEntryDate = db.Column(db.String(150))
    TestEntryTime = db.Column(db.Float(15))
    TestEntryURL = db.Column(db.String(255))
    feed_url = db.Column(db.String, db.ForeignKey('Feed.feedURL'))


    def __init__(self, TestEntryTitle, TestEntrySummary, TestEntryDate, TestEntryTime, TestEntryURL):
        self.TestEntryTitle = TestEntryTitle
        self.TestEntrySummary = TestEntrySummary
        self.TestEntryDate = TestEntryDate
        self.TestEntryTime = TestEntryTime
        self.TestEntryURL = TestEntryURL;
