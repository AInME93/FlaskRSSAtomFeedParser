# ########################################PARSER MODULE###################################################
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
from .. import db
from app.Feeds.models import Feed, FeedEntry,FeedEntryTest
from . import feeds

from multiprocessing import Pool
import time,feedparser

# FEEDS = Feed.query.options(load_only("feedURL")).all()  # List of dictionaries storing query results
# FEEDS = Feed.query.with_entities(Feed.feedURL).all()
# FEEDS = ['http://www.randompychance.wordpress.com/feed']
# FEEDS = Feed.query.all()  # List of dictionaries storing query results


def parallelParse(obj):
    '''
    This function performs the main task of the module, parsing feeds stored in the db and saving them in a list before 
    returning a list of lists of tuples containing feed entry details.
    '''
    parsed = []
    d = feedparser.parse(obj.feedURL, modified= obj.feedModified)
    modified = time.mktime(d.feed.get('modified_parsed', None))

    if modified != obj.feedModified:
        # Should create an object (possibly dictionary?) to append the new value of 'modified' to.

        for entry in d.entries:
            parsed.append(tuple((entry.title, entry.summary, entry.published, time.mktime(entry.published_parsed), entry.link,)))

    return parsed


def saveEntries(obj):
    '''
    For each parsed feed, for each entry in it, save the title/summary/date/epoch and url into the corresponding row
    in the database table.
    '''

    for i in range(len(obj)):
        for j in range(len(obj[i])):
            newFeedEntry = FeedEntryTest(TestEntryTitle=obj[i][j][0],TestEntrySummary = obj[i][j][1][:200],
                                         TestEntryDate=obj[i][j][2],
                                         TestEntryTime=obj[i][j][3],
                                         TestEntryURL=obj[i][j][4])
            db.session.add(newFeedEntry)
            db.session.commit()

def updateModified(obj):
     '''
     Should add logic here to check the values of 'modified' stored in the object from parsing function and update them
     in the 
     '''

@feeds.route('/')
def home():
    feed_entries = FeedEntryTest.query.order_by(FeedEntryTest.TestEntryTime.desc()).all()
    return render_template("main.html", feed_entries=feed_entries)

@feeds.route('/aggregate-now')
def parseModule():
    t1 = time.time()
    # Query the feed URL and Modified records and store them in a list of tuples
    FEEDS = db.session.query(Feed).all()
    print(time.time() - t1)

    t2 = time.time()
    # Spawn a pool of workers and map the parsing function to run among them
    pool = Pool(processes=1)
    result = pool.map(parallelParse,(item for item in FEEDS))
    print(time.time() - t2)

    saveEntries(result)


    feed_entries = FeedEntryTest.query.order_by(FeedEntryTest.TestEntryTime.desc()).all()
    return render_template("main.html", feed_entries = feed_entries)



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
                    newFeedEntry = FeedEntryTest(TestEntryTitle=entry.title, TestEntrySummary=entry.summary_detail.value,
                                                 TestEntryDate=entry.published,
                                                 TestEntryTime=time.mktime(entry.published_parsed))
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
                newFeedEntry = FeedEntryTest(TestEntryTitle=entry.title, TestEntrySummary=entry.summary_detail.value,
                                             TestEntryDate=entry.published,
                                             TestEntryTime=time.mktime(entry.published_parsed))
                db.session.add(newFeedEntry)
                db.session.commit()

"""

