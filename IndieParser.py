from PageParser import PageParser
from datetime import datetime
import re
from bs4 import BeautifulSoup
from ShowDB import VenueEvent

class IndieParser(PageParser):

    m_siteDomain = 'http://www.theindependentsf.com'

    def getVenue(self):
        return Venue(name = 'The Independent', link = m_siteDomain)

    def parse(self, pageText):

        event_blocks = []

        soup = BeautifulSoup(pageText)
        if soup == None:
            # throw something
            return None

        event_blocks = soup.find_all("div", re.compile("list-view-item"))

        for event in event_blocks:

            if event != None:
                ed = dict()

                headline_summary = event.find("h1", "headliners summary").a
                if headline_summary != None:
                    # error no openers in log
                    ed['headliners'] = headline_summary.string.encode('utf-8')
                    ed['headliners_link'] = self.formURL(headline_summary['href'], self.m_siteDomain)


                eInfo = event.find("h2", "topline-info")
                if eInfo != None:
                    ed['event_info'] = u' '.join(eInfo.strings).encode('utf-8')
                else:
                    ed['event_info'] = u''

                headliners = event.find("h1", "headliners").a
                if headliners != None:
                    ed['openers'] = headliners.string.encode('utf-8')

                openers = event.find("h2", "supports description")
                if openers != None:
                    ed['openers'] = u' '.join([openers.a.string, ed['openers']]).encode('utf-8')
                    ed['openers_link'] = self.formURL(openers.a['href'], self.m_siteDomain)
                else:
                    # report no openers in log
                    ed['openers'] = ''
                    ed['openers_link'] = ''

                indieDate = event.find("span", "value-title")['title']
                #if show_date == None:
                    # throw no date exception
                ed['event_datetime'] = self.makeDatetime(indieDate)

                price = event.find("h3", "price-range")
                if price != None:
                    ed['price'] = price.string.strip().encode('utf-8')
                else:
                    ed['price'] = 'See website for details'

                # add data to database session
                myEV = VenueEvent(headliner = ed['headliners'], event_info = ed['event_info'], headliner_link = ed['headliners_link'], openers = ed['openers'], openers_link = ed['openers_link'], event_datetime = ed['event_datetime'], event_price = ed['price'])
                self.events.append(myEV)

        return self.events

    def makeDatetime(self, indieDate):

        reDate = re.search('([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+):[0-9]+-([0-9]+):[0-9]+', indieDate)
        if reDate == None:
            return None

        event_date = datetime(int(reDate.group(1)), int(reDate.group(2)), int(reDate.group(3)), int(reDate.group(4)), int(reDate.group(5)))
        return event_date
