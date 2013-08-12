from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Integer, Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref, sessionmaker

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
    name = Column(String(128))
    link = Column(String(256))
    phone_num = Column(String(16))
    address = Column(String(256))
    events = relationship("VenueEvent", backref=backref('venue', order_by=id))

    def __init__(self):
        return

class VenueEvent(Base):

    __tablename__ = 'venueEvent'
    id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
    event_comment = Column(String(512))
    headliner = Column(String(128))
    headliner_link = Column(String(256))
    event_info = Column(String(512))
    openers = Column(String(256))
    openers_link = Column(String(256))
    event_datetime = Column(DateTime)
    event_price = Column(String(128))

    venue_id = Column(Integer, ForeignKey('venue.id'))
