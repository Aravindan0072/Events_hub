import os
import re
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("EVENTBRITE_TOKEN")

# ✅ THE BING PROXY
def search_bing_for_links(site, city, keyword, limit=15):
    """
    Scrapes Bing Search results to find Eventbrite links.
    """
    print(f"🔎 Bing-Proxy: Searching {site} for {city}...")
    
    # 1. Fake a real browser (Bing allows this)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 2. Build Query
    query = f'site:{site} "{city}" "{keyword}"'
    url = f"https://www.bing.com/search?q={query}"
    
    found_ids = set()
    
    try:
        # 3. Hit Bing
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"   ❌ Bing Blocked: {res.status_code}")
            return []
            
        # 4. Extract Links
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Bing standard result selector
        results = soup.select("li.b_algo h2 a")
        
        for link in results:
            href = link.get("href")
            
            # EXTRACT ID based on site
            if "eventbrite.com" in site:
                match = re.search(r'(\d{10,})', href)
                if match: found_ids.add(match.group(1))
                
        print(f"   🎯 Bing found {len(found_ids)} IDs for {site}")
        
    except Exception as e:
        print(f"   ❌ Bing Parsing Error: {e}")
        
    return list(found_ids)[:limit]

# ✅ THE API HYDRATOR
def fetch_eventbrite_details(event_id):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"expand": "venue,logo"}

    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200: return None
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
            "price": "Check Link",
            "is_free": data.get("is_free", False)
        }
    except: return None

# ✅ THE CONTROLLER
def get_bing_events():
    cities = ["chennai", "bangalore"]
    all_events = []
    
    for city in cities:
        # A. Eventbrite via Bing
        eb_ids = search_bing_for_links("eventbrite.com/e/", city, "Business")
        print(f"   ⚡ Hydrating {len(eb_ids)} Eventbrite events...")
        
        for eid in eb_ids:
            event = fetch_eventbrite_details(eid)
            if event:
                if event['city'] == "Unknown": event['city'] = city.title()
                all_events.append(event)
                print(f"      ✅ Saved EB: {event['title'][:30]}...")
            time.sleep(0.2)
            
    return all_events