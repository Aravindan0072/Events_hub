import os
import re
import requests
import time
from datetime import datetime
from googlesearch import search 
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("EVENTBRITE_TOKEN")

def get_eventbrite_ids_via_search(city):
    """
    Asks Google for Eventbrite links.
    """
    print(f"🔎 Google-Hacking for {city} events...")
    found_ids = set()
    
    # 1. The Query
    query = f'site:eventbrite.com/e/ "{city}" "Business" OR "Tech"'
    
    try:
        # ✅ FIX: Call search() without 'num' or 'stop' arguments.
        # We loop through the results and manually break after 15 items.
        count = 0
        limit = 15
        
        # 'search' returns an infinite stream of links, we grab the first 15
        for url in search(query): 
            if count >= limit:
                break
                
            # Regex to steal the Event ID
            match = re.search(r'(\d{10,})', url)
            if match:
                found_ids.add(match.group(1))
                count += 1
                
        print(f"   🎯 Google found {len(found_ids)} Event IDs.")
        
    except Exception as e:
        print(f"   ❌ Search Error: {e}")
        
    return list(found_ids)

def fetch_eventbrite_details(event_id):
    """
    Uses your OFFICIAL API Token to get perfect data.
    """
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"expand": "venue,logo,ticket_availability"}

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
            "price": "Free" if data.get("is_free") else "Check Link",
            "is_free": data.get("is_free", False)
        }
    except: return None

# --- CONTROLLER ---
def get_smart_events():
    cities = ["chennai", "bangalore"]
    all_events = []
    
    for city in cities:
        ids = get_eventbrite_ids_via_search(city)
        
        print(f"   ⚡ Fetching details for {len(ids)} events...")
        for eid in ids:
            event = fetch_eventbrite_details(eid)
            if event:
                if event['city'] == "Unknown": event['city'] = city.title()
                all_events.append(event)
                print(f"      ✅ Saved: {event['title'][:30]}...")
            time.sleep(0.5) 
            
    return all_events