from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    date_text = Column(String)
    location = Column(String)
    city = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(String, default="Business")
    price = Column(String, default="Check Link")
    is_free = Column(Boolean, default=False)
    
    # Internal vs External (Scraped)
    source_type = Column(String, default="external") # 'internal' or 'external'
    external_url = Column(String, nullable=True)     # Link to AllEvents/Eventbrite
    
    # Analytics (Section D of your plan)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)