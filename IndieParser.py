from PageParser import PageParser
from datetime import datetime
import re
from bs4 import BeautifulSoup

class IndieParser(PageParser):

    m_siteDomain = 'http://www.theindependentsf.com'

    def parse(self, pageText):

        pageData = []
        event_blocks = []

        soup = BeautifulSoup(pageText)
        # eventData['title'] = soup.html.head.title.string

        event_blocks = soup.find_all("div", "list-view-details vevent")

        for event in event_blocks:

            if event != None:
                eventData = dict()

                headline_summary = event.find("h1", "headliners summary").a
                #if headliners == None:
                    # error no openers in log
                eventData['headliners'] =headline_summary.string
                eventData['headliners_link'] = self.formURL(headline_summary['href'], self.m_siteDomain)

                headliners = event.find("h1", "headliners").a
                if headliners != None:
                    eventData['headliners'] += " " +  headliners.string

                event_info = event.find("h2", "topline-info")
                if event_info != None:
                    eventData['event_info'] = ''
                    for info in event_info.strings:
                        eventData['event_info'] += info + ' '
                        print eventData['event_info']

                openers = event.find("h2", "supports description")
                if openers != None:
                    eventData['openers'] = openers.a.string
                    eventData['openers_link'] = self.formURL(openers.a['href'], self.m_siteDomain)
                # else
                    # report no openers in log

                indieDate = event.find("span", "value-title")['title']
                #if show_date == None:
                    # throw no date exception
                eventData['event_datetime'] = self.cleanupDatetime(indieDate)

                pageData.append(eventData)

        return pageData

    def cleanupDatetime(self, indieDate):

        reDate = re.search('([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9])', indieDate)
        if reDate == None:
            return None

        event_date = datetime(int(reDate.group(1)), int(reDate.group(2)), int(reDate.group(3)), int(reDate.group(4)), int(reDate.group(5)))
        return event_date
