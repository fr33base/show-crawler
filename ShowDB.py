from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class ShowDB:


    def __init__(self, dbInfo):

        self.engine = create_engine('sqlite:///:memory:', echo=True)
        return

    def feed(self, pageData):
        return

class Venue(Base):

    __tablename__ = 'venue'
    id = Column(Integer, Sequence('venue_id_seq'), primary_key=True)
    name = Column(String)
    link = Column(String)
    phone_num = Column(String)
    address = Column(String)
    events = relationship("VenueEvent", backref=backref('venue', order_by=id))

    def __init__(self):
        return

class VenueEvent(Base):

    __tablename__ = 'venueEvent'
    id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
    event_comment = Column(String)
    headliner = Column(String)
    headliner_link = Column(String)
    event_info = Column(String)
    openers = Column(String)
    openers_link = Column(String)
    event_datetime = Column(DateTime)

    venue_id = Column(Integer, ForeignKey('venue.id'))
