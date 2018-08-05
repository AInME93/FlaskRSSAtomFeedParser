from flask_login import current_user
from sqlalchemy.orm import lazyload
from werkzeug.utils import redirect

from app import db
from app.models import *
from . import users
from flask import render_template, flash, url_for, request, session
from flask_security import login_required
from app.forms import RegisterFeedForm

# Views

@login_required
@users.route('/feeds')
def feedstimeline():
    feed_entries = FeedEntry.query.order_by(FeedEntry.EntryTime.desc()).all()
    return render_template("log_main.html", feed_entries = feed_entries)


@login_required
@users.route('/my-feeds')
def show_my_feeds():
    #
    # feed_list=[]
    #
    # feeds = Feed.query.all()
    # for feed in feeds:
    #     print(feed.FeedEntries)
    #
    #     feed_list.append(feed)

    feed_entries = current_user.followed_posts()
    for e in feed_entries:
        print(e)

    return render_template('log_main.html', feed_entries=feed_entries)


# @login_required
# @users.route('/feeds-list')
# def listFeeds():
#
#     # categories = [
#     #     'News',
#     #     'Sports'
#     #     'Creative Writing'
#     #     'Technology'
#     # ]
#
#     feeds = Feed.query.order_by(Feed.feedCategory).all()
#     return render_template("list.html", feeds=feeds)


@login_required
@users.route('/feeds-list')
def listFeeds():
    subsId = []
    subs = current_user.subscriptions.all()

    for e in subs:
        subsId.append(e.id)

    feeds = db.session.query(Feed).filter(Feed.id.notin_(subsId))
    # feeds = Feed.query.filter_by(Feed.id != subs.e.id).order_by(Feed.feedCategory).all()
    return render_template("list.html", feeds=feeds)



@login_required
@users.route('/my-feeds-list')
def list_my_feeds():
    feeds = current_user.subscriptions.all()

    if feeds is None:
        flash('You dont seem to have subscribed to any feed yet.')
        return redirect(url_for('feedstimeline'))

    return render_template('subscribed_list.html', feeds = feeds)

@login_required
@users.route('/subscribe/<feed_id>')
def follow(feed_id):
    feed = Feed.query.filter_by(id=feed_id).first()

    if feed is None:
        flash('Sorry that feed cannot be found.')
        return redirect(url_for('feedstimeline'))

    current_user.subscribe(feed)
    db.session.commit()
    flash('You are subscribed to {}!'.format(Feed.feedTitle))
    return redirect(request.referrer)


@login_required
@users.route('/vote/<entry_id>')
def like(entry_id):
    entry = FeedEntry.query.filter_by(id=entry_id).first()

    if entry is None:
        flash('Sorry that entry cannot be found.')
        return redirect(url_for('feedstimeline'))

    current_user.votepost(entry)
    db.session.commit()
    flash('Thanks!')
    return redirect(request.referrer)

@login_required
@users.route('/save/<entry_id>')
def save(entry_id):
    entry = FeedEntry.query.filter_by(id=entry_id).first()

    if entry is None:
        flash('Sorry that entry cannot be found.')
        return redirect(url_for('feedstimeline'))

    current_user.savepost(entry)
    db.session.commit()
    flash('Thanks!')
    return redirect(request.referrer)

@login_required
@users.route('/saved-posts')
def show_my_saves():

    feed_entries = current_user.savedposts.all()
    return render_template('log_main.html', feed_entries=feed_entries)

@login_required
@users.route('/register-feed', methods = ['GET','POST'])
def register_feed():
    form = RegisterFeedForm(request.form)
    if request.method == 'POST' and form.validate():
        feed = Feed( feedTitle = form.feedTitle.data, feedURL = form.feedURL.data,\
                    feedCategory = form.feedCategory.data,feedDescription = form.feedDescription.data)
        db.session.add(feed)
        db.session.commit

        flash('Success! Thanks for registering a new feed!')
        return redirect('/register-feed')
    return render_template('register_feed.html', form=form)

# @users.route('/register', methods = ['POST'])
# @login_required
# def register():
#     return render_template('security/register_user.html')
#
# @users.route('/login')
# @login_required
# def logging_in():
#     return render_template('security/register_user.html')