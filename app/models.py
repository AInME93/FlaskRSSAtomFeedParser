from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from flask_security import UserMixin, RoleMixin
from app import db


# Define models
roles_users = db.Table('roles_users',
        # db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
        db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('Role.id'))
       )

# Implement many-to-many relationship between users and feeds

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('Feed.id'))
)

# Implement many-to-many vote relationship between users and feeds entries
votes = db.Table('votes',
    db.Column('voter_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('FeedEntry.id'))
)


# Implement many-to-many relationship between users and feeds entries

saves = db.Table('saves',
    db.Column('saver_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('FeedEntry.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = "Role"
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    subscriptions = db.relationship('Feed', secondary=followers,
        backref=db.backref('subscribers', lazy='dynamic'), lazy = 'dynamic')

    votedposts = db.relationship('FeedEntry', secondary=votes,
        backref=db.backref('voters', lazy='dynamic'), lazy = 'dynamic')

    savedposts = db.relationship('FeedEntry', secondary=saves,
        backref=db.backref('savers', lazy='dynamic'), lazy = 'dynamic')

    def subscribe(self, feed):
        if not self.is_subscribed(feed):
            self.subscriptions.append(feed)
        else:
            self.subscriptions.remove(feed)

    # Query on the followers relationship to check if a link between the user and feed already exists.
    def is_subscribed(self, feed):
        return self.subscriptions.filter(
            followers.c.feed_id == feed.id).count() > 0

    def followed_posts(self):
        return FeedEntry.query.join(
            followers, (followers.c.feed_id == FeedEntry.feed_id)).filter(
            followers.c.follower_id == self.id).order_by(
            FeedEntry.EntryTime.desc())
    #
    # def vote(self, feed):
    #     if not self.has_voted(feed):
    #         self.votes.append(feed)
    #
    # def unsubscribe(self, feed):
    #     if self.has_voted(feed):
    #         self.votes.remove(feed)
    #
    # # Query on the followers relationship to check if a link between the user and feed already exists.
    # def has_voted(self, feed):
    #     return self.subscriptions.filter(
    #         followers.c.feed_id == feed.id).count() > 0

    def votepost(self, feedEntry):
        if not self.has_voted(feedEntry):
            self.votedposts.append(feedEntry)
        else:
            self.votedposts.remove(feedEntry)

    # Query on the followers relationship to check if a link between the user and feed already exists.
    def has_voted(self, feedEntry):
        return self.votedposts.filter(
            votes.c.entry_id == feedEntry.id).count() > 0

    def savepost(self, feedEntry):
        if not self.has_saved(feedEntry):
            self.savedposts.append(feedEntry)
        else:
            self.savedposts.remove(feedEntry)

    # Query on the followers relationship to check if a link between the user and feed already exists.
    def has_saved(self, feedEntry):
        return self.savedposts.filter(
            saves.c.entry_id == feedEntry.id).count() > 0

# Model for feed with a one-to-many relationship with feed entries

class Feed(db.Model):
    __tablename__ = "Feed"
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    feedTitle = db.Column(db.String(150))
    feedDescription = db.Column(db.String(255))
    feedURL = db.Column(db.String(255), unique = True)
    feedCategory = db.Column(db.String(255))
    feedModified = db.Column(db.String(35), default ='0.0')
    feedEtag = db.Column(db.String, nullable=True)
    FeedEntries = db.relationship('FeedEntry', backref='origin_feed',
                                lazy='dynamic')

    # def __init__(self, feedTitle, feedURL, feedCategory, feedDescription, feedModified, feedEtag, FeedEntries):
    #     self.feedTitle = feedTitle;
    #     self.feedURL = feedURL;
    #     self.feedCategory = feedCategory;
    #     self.feedModified = feedModified;
    #     self.feedDescription = feedDescription;
    #     self.feedEtag = feedEtag;
    #     self.FeedEntries = FeedEntries;




class FeedEntry(db.Model):
    __tablename__ = "FeedEntry"
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    EntryFeedTitle = db.Column(db.String(150))
    EntryTitle = db.Column(db.String(255))
    EntrySummary = db.Column(db.String(255))
    EntryURL = db.Column(db.String(255))
    EntryDate = db.Column(db.DateTime(255))
    EntryTime = db.Column(db.Float(15), default = 0.0)
    EntryCategory = db.Column(db.String(255))
    feed_id = db.Column(db.Integer, db.ForeignKey('Feed.id'))

    # def __init__(self, EntryFeedTitle, EntryTitle, EntrySummary, EntryURL, EntryDate, EntryTime, EntryCategory):
    #     self.EntryFeedTitle = EntryFeedTitle;
    #     self.EntryTitle = EntryTitle;
    #     self.EntrySummary = EntrySummary;
    #     self.EntryURL = EntryURL;
    #     self.EntryDate = EntryDate;
    #     self.EntryTime = EntryTime;
    #     self.EntryCategory = EntryCategory;


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