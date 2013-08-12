from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Integer, Column, Boolean, Unicode, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()

class ShowDB:
    Session = sessionmaker()

    def __init__(self, dbInfo):

        if dbInfo == 'test':
            self.engine = create_engine('sqlite:///:memory:', echo=False)
        else:
            self.engine = create_engine('mysql+mysqldb://will:showcrawling@localhost/showcrawler?charset=utf8', echo=True, pool_recycle=3600)
# db error checking
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
# db create error checking
        return

    def feed(self, dbObj):
        session = self.Session()
        session.add_all(dbObj)
        session.commit()
        # do some redundency checking
        return

class Venue(Base):

    __tablename__ = 'venue'
    id = Column(Integer, Sequence('venue_id_seq'), primary_key=True)
    name = Column(Unicode)
    link = Column(Unicode)
    phone_num = Column(Unicode)
    address = Column(Unicode)
    events = relationship("VenueEvent", backref=backref('venue', order_by=id))

    def __init__(self):
        return

class VenueEvent(Base):

    __tablename__ = 'venueEvent'
    id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
    event_comment = Column(Unicode)
    comment_dirty = Column(Boolean, default=False)
    headliner = Column(Unicode)
    headliner_dirty = Column(Boolean, default=False)
    headliner_link = Column(Unicode)
    event_info = Column(Unicode)
    info_dirty = Column(Boolean, default=False)
    openers = Column(Unicode)
    openers_dirty = Column(Boolean, default=False)
    openers_link = Column(Unicode)
    event_datetime = Column(DateTime)
    event_time_dirty = Column(Boolean, default=False)
    last_updated = Column(DateTime, onupdate=datetime.now)
    created_date = Column(DateTime, default=datetime.now)
    event_deleted = Column(Boolean, default=False)

    venue_id = Column(Integer, ForeignKey('venue.id'))
