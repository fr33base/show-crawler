from PageParser import PageParser
from datetime import datetime
import re
from bs4 import BeautifulSoup
from ShowDB import VenueEvent

class IndieParser(PageParser):

    m_siteDomain = 'http://www.theindependentsf.com'

    def parse(self, pageText):

        event_blocks = []

        soup = BeautifulSoup(pageText)
        if soup == None:
            # throw something
            return None

        event_blocks = soup.find_all("div", "list-view-details vevent")

        for event in event_blocks:

            if event != None:
                ed = dict()

                headline_summary = event.find("h1", "headliners summary").a
                #if headliners == None:
                    # error no openers in log
                ed['headliners'] =headline_summary.string
                ed['headliners_link'] = self.formURL(headline_summary['href'], self.m_siteDomain)

                headliners = event.find("h1", "headliners").a
                if headliners != None:
                    ed['headliners'] += " " +  headliners.string

                eInfo = event.find("h2", "topline-info")
                if eInfo != None:
                    ed['event_info'] = ''
                    for info in eInfo.strings:
                        ed['event_info'] += info + ' '
                else:
                    ed['event_info'] = ''

                openers = event.find("h2", "supports description")
                if openers != None:
                    ed['openers'] = openers.a.string
                    ed['openers_link'] = self.formURL(openers.a['href'], self.m_siteDomain)
                else:
                    # report no openers in log
                    ed['openers'] = ''
                    ed['openers_link'] = ''

                indieDate = event.find("span", "value-title")['title']
                #if show_date == None:
                    # throw no date exception
                ed['event_datetime'] = self.cleanupDatetime(indieDate)

                # add data to database session
                myEV = VenueEvent(headliner = ed['headliners'], event_info = ed['event_info'], headliner_link = ed['headliners_link'], openers = ed['openers'], openers_link = ed['openers_link'], event_datetime = ed['event_datetime'])
                self.events.append(myEV)

        return self.events

    def cleanupDatetime(self, indieDate):

        reDate = re.search('([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+):[0-9]+-([0-9]+):[0-9]+', indieDate)
        if reDate == None:
            return None

        event_date = datetime(int(reDate.group(1)), int(reDate.group(2)), int(reDate.group(3)), int(reDate.group(4)), int(reDate.group(5)))
        return event_date
