import os
import re
import requests
import time
import json
import psutil # Needs pip install psutil
from datetime import datetime
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("EVENTBRITE_TOKEN")

# --- PART 0: CLEANUP WINDOWS LOCKS ---
def kill_stuck_chrome():
    """
    Force kills old chrome processes to fix WinError 183
    """
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                try:
                    proc.kill()
                except: pass
    except: pass

# --- PART 1: THE STEALTH BROWSER ---
def get_scraper_driver():
    # 1. Kill old locks first
    kill_stuck_chrome()
    time.sleep(1)

    print("👻 Launching Stealth Browser...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Retry mechanism for the 183 Error
    for attempt in range(3):
        try:
            driver = uc.Chrome(options=options, use_subprocess=True)
            return driver
        except Exception as e:
            print(f"   ⚠️ Driver Start failed (Attempt {attempt+1}/3). Retrying...")
            time.sleep(2)
            kill_stuck_chrome()
            
    raise Exception("Could not start Chrome after 3 attempts.")

# --- PART 2: EVENTBRITE LOGIC ---
def get_eventbrite_ids(driver, city):
    found_ids = set()
    try:
        # We use a broad search to ensure we get results
        url = f"https://www.eventbrite.com/d/{city}/events/"
        print(f"🚀 Navigating to Eventbrite: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Scroll down
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.select("a[href*='/e/']")
        for link in links:
            match = re.search(r'(\d{10,})', link['href'])
            if match: found_ids.add(match.group(1))
            
        print(f"   🎯 Found {len(found_ids)} Eventbrite IDs in {city}")
    except Exception as e:
        print(f"   ❌ Eventbrite Error: {e}")
    return list(found_ids)

def fetch_eventbrite_api(event_id):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"expand": "venue,logo,ticket_availability"}

    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200: 
            print(f"   ⚠️ API Skip {event_id}: Status {res.status_code}")
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
        return None

# --- PART 3: MEETUP LOGIC ---
def scrape_meetup(driver, city):
    print(f"🚀 Navigating to Meetup: {city}...")
    events = []
    try:
        url = f"https://www.meetup.com/find/?keywords=tech&location=us--{city[0:2]}--{city}"
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                if "itemListElement" in data:
                    for entry in data["itemListElement"]:
                        item = entry.get("item", {})
                        if item.get("@type") == "Event":
                            events.append({
                                "title": item.get("name"),
                                "description": item.get("description", "Meetup Event"),
                                "date_text": item.get("startDate", "Upcoming").replace("T", " "),
                                "location": item.get("location", {}).get("name", city.title()),
                                "city": city.title(),
                                "image_url": item.get("image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7"),
                                "category": "Technology",
                                "source_type": "external",
                                "external_url": item.get("url"),
                                "price": "Check Link",
                                "is_free": False
                            })
            except: continue
        print(f"   🎯 Found {len(events)} Meetup Events in {city}")
    except Exception as e:
        print(f"   ❌ Meetup Error: {e}")
    return events

# --- PART 4: CONTROLLER ---
def get_hybrid_events():
    cities = ["chennai", "bangalore"]
    all_events = []
    
    driver = None
    try:
        driver = get_scraper_driver()
        
        for city in cities:
            # 1. Get Eventbrite
            eb_ids = get_eventbrite_ids(driver, city)
            print(f"   ⚡ Processing {len(eb_ids)} Eventbrite IDs via API...")
            
            for eid in eb_ids:
                data = fetch_eventbrite_api(eid)
                if data: 
                    if data['city'] == "Unknown": data['city'] = city.title()
                    all_events.append(data)
                    print(f"      ✅ Saved EB: {data['title'][:20]}...")
                time.sleep(0.1) # Be nice to API
            
            # 2. Get Meetup
            meetup_data = scrape_meetup(driver, city)
            all_events.extend(meetup_data)
            
    except Exception as e:
        print(f"❌ Critical Scraper Error: {e}")
    finally:
        if driver:
            try: driver.quit()
            except: pass
        
    return all_events