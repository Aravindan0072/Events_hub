import undetected_chromedriver as uc
import time
import requests 
import os
import psutil
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("EVENTBRITE_TOKEN")

# ✅ 1. THE CLEANER (Fixes stuck Chrome processes)
def force_kill_chrome():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                proc.kill()
        except: pass
    time.sleep(1)

# ✅ 2. THE CYBORG BROWSER (Finds Event IDs)
def get_event_ids_via_cyborg(city):
    force_kill_chrome()
    print("🤖 Launching Cyborg Browser...")
    
    options = uc.ChromeOptions()
    options.headless = False  # Visible window so you can solve CAPTCHA
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    found_ids = set()
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        
        # Go to Eventbrite
        url = f"https://www.eventbrite.com/d/{city}/business--events/"
        print(f"🚀 Navigating to: {url}")
        driver.get(url)
        
        # SMART WAIT
        print("👀 Waiting for events... (SOLVE CAPTCHA IF NEEDED)")
        for i in range(10): # Wait up to 50 seconds
            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.select("a[href*='/e/']")
            if len(links) > 0:
                print(f"   ✅ Access Granted! Found {len(links)} raw links.")
                break
            time.sleep(5)
            
        # EXTRACT IDs ONLY 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.select("a[href*='/e/']")
        
        for link in links:
            href = link.get('href')
            if '-' in href:
                # Example: .../e/my-event-123456789 -> 123456789
                try:
                    event_id = href.split('-')[-1].split('?')[0] # Clean ID
                    if event_id.isdigit():
                        found_ids.add(event_id)
                except: pass
                
        print(f"   🎯 Extracted {len(found_ids)} Unique Event IDs.")
        
    except Exception as e:
        print(f"❌ Cyborg Error: {e}")
    finally:
        if driver:
            print("👋 Closing Browser...")
            driver.quit()
            
    return list(found_ids)

# ✅ 3. THE API HYDRATOR (Gets Details + DEBUGGING)
def fetch_event_details(event_id):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"expand": "venue,logo,ticket_availability"}

    try:
        # Debug: Print that we are trying
        # print(f"      ❓ Asking API for ID: {event_id}...") 

        res = requests.get(url, headers=headers, params=params)
        
        # 🛑 IF API FAILS, PRINT THE ERROR CODE
        if res.status_code != 200: 
            print(f"      ❌ API Refused ID {event_id}: Status {res.status_code}")
            # print(f"         Reason: {res.text[:100]}") # Show detail if needed
            return None
            
        data = res.json()
        
        return {
            "title": data.get("name", {}).get("text"),
            "description": data.get("description", {}).get("text"),
            "date_text": datetime.fromisoformat(data["start"]["local"]).strftime("%b %d • %I:%M %p"),
            "location": data.get("venue", {}).get("name", "Online"),
            "city": data.get("venue", {}).get("address", {}).get("city", "Unknown"),
            "image_url": data.get("logo", {}).get("url") if data.get("logo") else None,
            "category": "Business",
            "source_type": "external",
            "external_url": data.get("url"),
            "price": "Free" if data.get("is_free") else "Check Link",
            "is_free": data.get("is_free", False)
        }
    except Exception as e: 
        print(f"      ❌ Python Error: {e}")
        return None

# ✅ 4. THE CONTROLLER
def get_cyborg_events():
    all_events = []
    cities = ["chennai", "bangalore"]
    
    for city in cities:
        # A. Get IDs (Cyborg)
        ids = get_event_ids_via_cyborg(city)
        
        # B. Get Details (API)
        print(f"   ⚡ Fetching details for {len(ids)} events via API...")
        for eid in ids:
            event = fetch_event_details(eid)
            if event:
                if event['city'] == "Unknown": event['city'] = city.title()
                all_events.append(event)
                print(f"      ✅ Saved: {event['title'][:30]}...")
            time.sleep(0.1)
            
    return all_events