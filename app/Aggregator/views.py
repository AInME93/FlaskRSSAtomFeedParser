# ########################################PARSER MODULE################################################################
# This module implements the main function of the application which is to parse feed urls stored in the database and
# storing the entries found in them back in the database. Because the parsing is highly CPU-intensive, multiprocessing
# will be implemented to allow for parallel parsing of several feed urls at a time.
#
# Multiprocessing uses pickle and therefore arguments passed to the multiprocessing process need to be picklable as
# explained in this article: https://pymotw.com/2/multiprocessing/basics.html , meaning app_context, lambda functions,
# among other objects cannot be passed as arguments.
#
# Entities will be pulled from the Feeds table including values of the url, category and modified and be stored into a
# python list and stored in a file. The parser function will retrieve these values from the file and perform the parsing
#  and recording of entries into another table in the database. To save bandwidth and reduce processing overhead, the
# feed's last stored modified value will be passed to the parsing function and compared with the current modified value
# as stored in the RSS/Atom feed file. If they are equal (status = 304), no entries will be stored as no new posts have
# been published since the feed was last parsed.
#
# As for those feeds whose modified value has changed, the new entries will be stored, and the new value of 'modified'
# field updated in the Feeds table.
#


from flask import render_template
from app.models import db, votes
from app.models import Feed, FeedEntry
from . import feeds
from flask_security import login_required

from multiprocessing import Pool
import time,feedparser

# FEEDS = Feed.query.options(load_only("feedURL")).all()  # List of dictionaries storing query results
# FEEDS = Feed.query.with_entities(Feed.feedURL).all()
# FEEDS = ['http://www.randompychance.wordpress.com/feed']
# FEEDS = Feed.query.all()  # List of dictionaries storing query results


@feeds.route('/')
def home():
    feed_entries = db.session.query(FeedEntry, db.func.count(votes.c.entry_id).label('TotalVotes')).outerjoin(votes, votes.c.entry_id == FeedEntry.id)\
        .order_by(FeedEntry.EntryTime.desc())\
        .group_by(FeedEntry.id)\
        .all()

    for fe in feed_entries:
        print(fe.FeedEntry.id, fe.FeedEntry.EntryTime, fe.TotalVotes)

    # feed_entries = FeedEntry.query.order_by(FeedEntry.EntryTime.desc()).all()
    return render_template("main.html", feed_entries=feed_entries)



@feeds.route('/aggregate-now')
def parseModule():
    t1 = time.time()
    # Query the feed URL and Modified records and store them in a list of tuples
    FEEDS = db.session.query(Feed).all()
    print(time.time() - t1)


    # Spawn a pool of workers and map the parsing function to run among them

    pool = Pool(processes=6)
    result = pool.map(parallelParse,(item for item in FEEDS))
    print("Parsing time: ", time.time() - t1)
    pool.close()

    t1 = time.time()
    saveEntries(result)
    t2 = time.time()
    feed_entries = FeedEntry.query.order_by(FeedEntry.EntryTime.desc()).all()
    return render_template("main.html", feed_entries = feed_entries)



def parallelParse(obj):
    '''
    This function performs the main task of the module, parsing feeds stored in the db and saving them in a list before
    returning a list of lists of tuples containing feed entry details.
    '''
    parsed = []
    newmodified = []
    d = feedparser.parse(obj.feedURL)
    try:
        modified = d.feed.published_parsed

    except AttributeError:
        modified= d.feed.get('modified_parsed', None)
        print('Modified for feed ', obj.feedURL, ' is: ', modified)


    modified = time.mktime(modified)
    print('Modified for feed ', obj.feedURL, ' is: ', modified)



    if modified != float(obj.feedModified):
        newmodified.append(tuple((obj.feedURL, modified, obj.feedTitle, obj.feedCategory)))
        for entry in d.entries:
            parsed.append(tuple((entry.title, entry.summary, entry.published, time.mktime(entry.published_parsed), entry.link, entry.id,)))


    return parsed, newmodified


def saveEntries(obj):
    '''
    For each parsed feed, for each entry in it, save the title/summary/date/epoch and url into the corresponding row
    in the database table.
    '''

    try:
        if obj[0][0]:
            values = range(len(obj))

        else:
            values = range(1, len(obj))

        for i in values:
            for j in range(len(obj[i][0])):
                entryvar = FeedEntry.query.filter_by(EntryURL = obj[i][0][j][4]).first()


                if entryvar is None:
                    feeds_entries = Feed.query.filter_by(feedURL = obj[i][1][0][0]).first()
                    newFeedEntry = FeedEntry(EntryFeedTitle=obj[i][1][0][2],
                                             EntryTitle=obj[i][0][j][0],
                                             EntrySummary = obj[i][0][j][1][:200],
                                             EntryDate=obj[i][0][j][2],
                                             EntryTime=obj[i][0][j][3],
                                             EntryURL=obj[i][0][j][4],
                                             EntryCategory=obj[i][1][0][3],
                                             origin_feed = feeds_entries)

                    db.session.add(newFeedEntry)
                    db.session.commit()

            feedUpdate = Feed.query.filter_by(feedURL = obj[i][1][0][0]).first()
            feedUpdate.feedModified = obj[i][1][0][1]
            db.session.commit()

    except IndexError as ie:
        print(ie)
        print('List is empty, possibly because all feeds haven\'t been modified since they were last parsed.')

'''
class threadedParser(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def record_feed_entry(self):

        feed_item = self.q.get()

        for feed_item.feedURL in feed_item:
            d = feedparser.parse(feed_item.feedURL)
            #d = feedparser.parse(feed_item.feedURL)

            modified = time.mktime(d.feed.get('modified_parsed', None))

            # Check to see if the feed has been modified since we last parsed it.
            # If it hasn't, then break, else record the new modified/etag value and save the newly published
            # entries into the database.
            print('modified = ', modified)
            print('feed_item_modified = ', feed_item.feedModified)

            if modified == feed_item.feedModified:
                break
            else:

                #Update the feed's modified value in the table
                feed_item.feedModified = modified
                db.session.commit()

                for entry in d.entries:
                    newFeedEntry = FeedEntry(EntryTitle=entry.title, EntrySummary=entry.summary_detail.value,
                                                 EntryDate=entry.published,
                                                 EntryTime=time.mktime(entry.published_parsed))
                    db.session.add(newFeedEntry)
                    db.session.commit()

        # Send signal to queue the task is done
        self.q.task_done()

    def main(self):
        # spawn a pool of threads, and pass them queue instance
        for i in range(10):
            t = threadedParser(q)
            t.setDaemon(True)
            t.start()

        # populate queue with data
        for feed_item in FEEDS:
            q.put(feed_item)

            # wait on the queue until everything has been processed
        q.join()

'''





"""
def parallelParsing():

    FEEDS = Feed.query.all()  # List of dictionaries storing query results

    for feed_item in FEEDS:
        d = feedparser.parse(feed_item.feedURL)

        modified = time.mktime(d.feed.get('modified_parsed', None))
        # etag = d.feed.get('etag', None)


        # Check to see if the feed has been modified since we last parsed it.
        # If it hasn't, then break, else record the new modified/etag value and save the newly published
        # entries into the database.
        print('modified = ', modified)
        print('feed_item_modified = ', feed_item.feedModified)

        if modified == feed_item.feedModified:
            break
        else:
            feed_item.feedModified = modified
            db.session.commit()

            for entry in d.entries:
                newFeedEntry = FeedEntry(EntryTitle=entry.title, EntrySummary=entry.summary_detail.value,
                                             EntryDate=entry.published,
                                             EntryTime=time.mktime(entry.published_parsed))
                db.session.add(newFeedEntry)
                db.session.commit()

"""

