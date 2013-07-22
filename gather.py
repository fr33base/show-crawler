from urllib2 import urlopen
from lxml import html

from IndieParser import IndieParser
from ShowDB import ShowDB

showDB = ShowDB("test")

# pageFile = urlopen("http://www.theindependentsf.com/")
pageFile = open('test_pages/indie.html', 'r')

page = pageFile.read()

indie = IndieParser()

eventList = indie.parse(page)

showDB.feed(eventList)
