#This module implements the main function of the application which is to parse feed urls stored in the database and storing the entries found
#in them back in the database. Because the parsing is highly CPU-intensive, multiprocessing will be implemented to allow for parallel parsing
#of several feed urls at a time.
#
#Multiprocessing uses pickle and therefore arguments passed to the multiprocessing process need to be picklable as explained in this article:
# https://pymotw.com/2/multiprocessing/basics.html , meaning app_context, lambda functions, among other objects cannot be passed as arguments.
#
#Entities will be pulled from the Feeds table including values of the url, category and modified and be stored into a python list and stored in
#a file. The parser function will retrieve these values from the file and perform the parsing and recording of entries into another table in
#the database. To save bandwidth and reduce processing overhead, the feed's last stored modified value will be passed to the parsing function
#and compared with the current modified value as stored in the RSS/Atom feed file. If they are equal (status = 304), no entries will be stored
#as no new posts have been published since the feed was last parsed.
#
#As for those feeds whose modified value has changed, the new entries will be stored, and the new value of 'modified' field updated in the Feeds
#table.
#.
# #

