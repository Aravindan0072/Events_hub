from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
# ✅ CHANGE 1: Use the CYBORG scraper (The one that works!)
import scraper_cyborg as scraper 
import registrar 
from database import engine, get_db

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.post("/api/refresh-events")
def refresh_events(db: Session = Depends(get_db)):
    """
    Triggers the Cyborg Scraper.
    This opens a browser window on the server for manual CAPTCHA solving.
    """
    # 1. Scrape Real Data using the Cyborg Browser
    try:
        # ✅ Call the cyborg function
        real_data = scraper.get_cyborg_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraper failed: {str(e)}")
    
    if not real_data:
        return {"status": "error", "message": "Cyborg found no events (Did you solve the CAPTCHA?)."}

    # 2. Clear ONLY old external events (keep internal user events)
    db.query(models.Event).filter(models.Event.source_type == "external").delete()
    
    # 3. Save new data
    new_count = 0
    for item in real_data:
        # Avoid duplicate titles if any slipped through
        event = models.Event(**item)
        db.add(event)
        new_count += 1
    
    db.commit()
    return {"status": "success", "added": new_count}

@app.get("/api/events", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    """
    Returns all events.
    """
    return db.query(models.Event).all()

@app.post("/api/events", response_model=schemas.EventResponse)
def create_internal_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    Allows a user to post their own event.
    """
    db_event = models.Event(**event.dict())
    db_event.source_type = "internal" # Force internal type
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/api/events/{event_id}", response_model=schemas.EventResponse)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """
    Gets details and increments VIEW count.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Increment View Count
    event.views += 1
    db.commit()
    db.refresh(event)
    
    return event

@app.post("/api/analytics/click/{event_id}")
def track_click(event_id: int, db: Session = Depends(get_db)):
    """
    Increments CLICK count when user clicks 'Register'.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        event.clicks += 1
        db.commit()
    return {"status": "tracked"}

@app.post("/api/register/{event_id}")
def auto_register(event_id: str, db: Session = Depends(get_db)):
    """
    Uses the Official API to register automatically.
    """
    result = registrar.register_for_event(event_id)
    if result["status"] == "success":
        return {"message": "✅ Successfully Registered! Check email."}
    else:
        return {"message": "❌ Failed. Use the link.", "error": result["message"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)