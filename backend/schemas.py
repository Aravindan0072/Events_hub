from pydantic import BaseModel
from typing import Optional

# Base Schema (Shared properties)
class EventBase(BaseModel):
    title: str
    description: str
    date_text: str
    location: str
    city: Optional[str] = None
    image_url: Optional[str] = None
    category: str
    price: Optional[str] = None
    is_free: bool = False
    external_url: Optional[str] = None

# Schema for creating an event (User input)
class EventCreate(EventBase):
    pass

# Schema for reading an event (Response to Frontend)
class EventResponse(EventBase):
    id: int
    source_type: str
    views: int
    clicks: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models