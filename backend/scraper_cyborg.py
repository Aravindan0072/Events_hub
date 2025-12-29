import undetected_chromedriver as uc
import time
import requests 
import os
import psutil
import random 
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("EVENTBRITE_TOKEN")

# ✅ 1. FALLBACK IMAGE PICKER (Only used if real image is missing)
def get_random_tech_image():
    images = [
        "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&q=80",
        "https://images.unsplash.com/photo-1559136555-930b723040bf?w=800&q=80",
        "https://images.unsplash.com/photo-1504384308090-c54be3855833?w=800&q=80",
    ]
    return random.choice(images)

# ✅ 2. THE CLEANER
def force_kill_chrome():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                proc.kill()
        except: pass
    time.sleep(1)

# ✅ 3. HELPER: LAUNCH BROWSER
def get_browser():
    force_kill_chrome()
    print("🤖 Launching Cyborg Browser...")
    options = uc.ChromeOptions()
    options.headless = False 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options, use_subprocess=True)

# ==========================================
# 🟠 EVENTBRITE SECTION (Real Images via API)
# ==========================================
def get_eventbrite_ids(driver, city):
    print(f"🟠 [Eventbrite] Searching in {city}...")
    found_ids = set()
    try:
        url = f"https://www.eventbrite.com/d/{city}/business--events/"
        driver.get(url)
        
        for i in range(10):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            if len(soup.select("a[href*='/e/']")) > 0: break
            time.sleep(3)
            
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for link in soup.select("a[href*='/e/']"):
            href = link.get('href')
            if '-' in href:
                try:
                    eid = href.split('-')[-1].split('?')[0]
                    if eid.isdigit(): found_ids.add(eid)
                except: pass
        print(f"   🎯 Found {len(found_ids)} Eventbrite IDs.")
    except Exception as e:
        print(f"   ❌ Eventbrite Error: {e}")
    return list(found_ids)

def fetch_eventbrite_details(event_id):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"expand": "venue,logo,ticket_availability"}
    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200: return None
        data = res.json()
        
        # Get Real Image
        img = data.get("logo", {}).get("url")
        if not img: img = get_random_tech_image() # Fallback

        return {
            "title": data.get("name", {}).get("text"),
            "description": data.get("description", {}).get("text"),
            "date_text": datetime.fromisoformat(data["start"]["local"]).strftime("%b %d • %I:%M %p"),
            "location": data.get("venue", {}).get("name", "Online"),
            "city": data.get("venue", {}).get("address", {}).get("city", "Unknown"),
            "image_url": img,
            "category": "Business",
            "source_type": "external",
            "external_url": data.get("url"),
            "price": "Free" if data.get("is_free") else "Check Link",
            "is_free": data.get("is_free", False)
        }
    except: return None

# ==========================================
# 🔵 MEETUP SECTION (Now With REAL Images)
# ==========================================
def scrape_meetup_cyborg(driver, city):
    print(f"🔵 [Meetup] Searching in {city}...")
    events = []
    try:
        url = f"https://www.meetup.com/find/?keywords=technology&location=in--{city}&source=EVENTS"
        driver.get(url)
        
        print("   👀 Scrolling to load Meetup events...")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
        soup = BeautifulSoup(driver.page_source, "html.parser")
        event_cards = soup.select("a[href*='/events/']")
        seen_urls = set()
        
        for link in event_cards:
            href = link.get('href')
            if "?" in href: href = href.split("?")[0]
            
            if href not in seen_urls and "http" in href:
                seen_urls.add(href)
                
                # 1. Get Title
                title_tag = link.find("h2") or link.find("h3") or link.find("span", class_="text-lg")
                title = title_tag.get_text(strip=True) if title_tag else "Tech Meetup"
                
                # 2. Get Time
                time_tag = link.find("time")
                date_text = time_tag.get_text(strip=True) if time_tag else "Upcoming"

                # 3. ✅ GET REAL IMAGE
                img_tag = link.find("img")
                real_image_url = None
                if img_tag:
                    real_image_url = img_tag.get("src") or img_tag.get("srcset", "").split(" ")[0]
                
                # Use real image if found, else random
                final_image = real_image_url if real_image_url else get_random_tech_image()

                events.append({
                    "title": title,
                    "description": "View full details on Meetup.com",
                    "date_text": date_text,
                    "location": city.title(),
                    "city": city.title(),
                    "image_url": final_image, # <--- REAL IMAGE!
                    "category": "Technology",
                    "source_type": "external",
                    "external_url": href,
                    "price": "Check Link",
                    "is_free": False
                })
                
        print(f"   🎯 Found {len(events)} Meetup Events.")
    except Exception as e:
        print(f"   ❌ Meetup Error: {e}")
    return events

# ==========================================
# 🚀 MAIN CONTROLLER
# ==========================================
def get_cyborg_events():
    all_events = []
    cities = [
    "chennai", "bangalore", "mumbai", "delhi", 
    "san-francisco", "new-york", "london", "dubai", 
    "singapore", "tokyo", "toronto", "berlin", 
    "sydney", "paris", "amsterdam"]
    driver = None
    try:
        driver = get_browser()
        for city in cities:
            # 1. Eventbrite
            eb_ids = get_eventbrite_ids(driver, city)
            for eid in eb_ids:
                data = fetch_eventbrite_details(eid)
                if data: 
                    if data['city'] == "Unknown": data['city'] = city.title()
                    all_events.append(data)
            
            # 2. Meetup
            mu_events = scrape_meetup_cyborg(driver, city)
            all_events.extend(mu_events)
    except Exception as e:
        print(f"❌ Global Error: {e}")
    finally:
        if driver:
            print("👋 Closing Cyborg Browser...")
            driver.quit()
    return all_events