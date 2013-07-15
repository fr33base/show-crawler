from urllib2 import urlopen
from lxml import html

from IndieParser import IndieParser
from ShowDB import ShowDB

showDB = ShowDB("database")

 # pageFile = urlopen("http://www.theindependentsf.com/")
pageFile = open('test_pages/indie.html', 'r')

page = pageFile.read()

indie = IndieParser()

pageData = indie.parse(page)

print pageData

showDB.feed(pageData)
