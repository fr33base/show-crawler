from PageParser import PageParser
from datetime import date
import re
from BeautifulSoup import BeautifulSoup

class IndieParser(PageParser):

    m_siteDomain = 'http://www.theindependentsf.com'

    def parse(self, pageText):

        pageData = dict()

        soup = BeautifulSoup(pageText)

        event = soup.find("div", "list-view-details vevent")

        if event != None:
            headline_summary = event.find("h1", "headliners summary").a.string
            pageData['headline_comment'] = headline_summary

            headliners = event.find("h1", "headliners").a
            #if headliners == None:
                # error no openers in log
            pageData['headliners'] = headliners.string
            pageData['headliners_link'] = self.formURL(headliners['href'], self.m_siteDomain)

            pageData['event_info'] = event.find("h2", "topline-info").string

            openers = event.find("h2", "supports description").a.string
            #if also_billed == None:
                # report no openers in log
            pageData['openers'] = openers

            event_datetime = self.cleanupDatetime(event.find("span", "value-title").string)
            #if show_date == None:
                # throw no date exception
            pageData['event_date'] = event_datetime.date
            pageData['event_time'] = event_datetime.time

# .find("h2", "topline-info").string

        #print top_info

        pageData['title'] = soup.html.head.title.string
        #pageData['event_comment'] = top_info

        return pageData

    def cleanupDate(self, indieDate):

        string.parse
        reDate = re.search('([0-9]+)\.([0-9]+)', indieDate)
        if reDate == None:
            return None

        event_date = date(int(currentYear), int(reDate.group(1)), int(reDate.group(2)))
        return event_date
