from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import datetime

# ✅ SCHEDULER IMPORTS
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager

import models, schemas
from database import engine, get_db, SessionLocal
import scraper_cyborg as scraper 
import registrar 

# Create Tables
models.Base.metadata.create_all(bind=engine)

# ==========================================
# ⏰ AUTOMATION TASK (The Night Shift)
# ==========================================
def auto_scrape_job():
    print(f"\n⏰ [12:00 AM] Auto-Scraper Started at {datetime.datetime.now()}")
    
    # 1. Create a fresh DB session
    db = SessionLocal()
    
    try:
        # 2. Run the Cyborg (Scrape World Data)
        print("   🚀 Launching Cyborg for Daily Update...")
        new_data = scraper.get_cyborg_events()
        
        # 3. SAFETY CHECK: Only update if we actually found events
        if new_data and len(new_data) > 0:
            print(f"   ✅ Scrape Successful! Found {len(new_data)} events.")
            
            # 4. Delete OLD External Events
            deleted = db.query(models.Event).filter(models.Event.source_type == "external").delete()
            print(f"   🗑️ Removed {deleted} old events.")
            
            # 5. Add NEW Events
            for item in new_data:
                db_event = models.Event(**item)
                db.add(db_event)
            
            db.commit()
            print("   💾 Database Updated Successfully!")
        else:
            print("   ⚠️ Scraper returned 0 events. Keeping old data to be safe.")
            
    except Exception as e:
        print(f"   ❌ Auto-Scrape Failed: {e}")
        db.rollback()
    finally:
        db.close()
        print("   💤 Job Finished. Waiting for next run.\n")

# ==========================================
# 🚀 LIFECYCLE (Start Scheduler on App Launch)
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule: Run every day at 00:00 (12 AM)
    scheduler.add_job(auto_scrape_job, CronTrigger(hour=0, minute=0))
    
    scheduler.start()
    print("✅ Daily Auto-Scraper Scheduled for 12:00 AM.")
    
    yield # App runs here...
    
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Enable CORS
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
    Manual Trigger (Button Click)
    """
    # Reuse the same logic? Or keep it simple.
    # For manual trigger, let's keep the direct approach for immediate feedback.
    db.query(models.Event).filter(models.Event.source_type == "external").delete()
    
    try:
        real_data = scraper.get_cyborg_events()
        if not real_data:
            return {"status": "warning", "message": "No events found."}

        for item in real_data:
            db.add(models.Event(**item))
        
        db.commit()
        return {"status": "success", "added": len(real_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@app.post("/api/events", response_model=schemas.EventResponse)
def create_internal_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.dict())
    db_event.source_type = "internal"
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/api/events/{event_id}", response_model=schemas.EventResponse)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event: raise HTTPException(status_code=404, detail="Not found")
    event.views += 1
    db.commit()
    db.refresh(event)
    return event

@app.post("/api/analytics/click/{event_id}")
def track_click(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        event.clicks += 1
        db.commit()
    return {"status": "tracked"}

@app.post("/api/register/{event_id}")
def auto_register(event_id: str, db: Session = Depends(get_db)):
    result = registrar.register_for_event(event_id)
    return {"message": "Success" if result["status"] == "success" else "Failed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)