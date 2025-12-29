import cloudscraper
from bs4 import BeautifulSoup
import json
import time
import random

# Initialize CloudScraper to bypass anti-bot protection
scraper = cloudscraper.create_scraper()

def scrape_eventbrite(city="san-francisco", category="business"):
    """
    Scrapes Eventbrite using Cloudscraper to bypass Cloudflare.
    Extracts data from JSON-LD tags for stability.
    """
    print(f"   Searching Eventbrite in {city} for {category}...")
    events = []
    
    # Eventbrite URL structure
    url = f"https://www.eventbrite.com/d/ca--{city}/{category}--events/"
    
    try:
        # 1. Fetch Search Page
        response = scraper.get(url)
        if response.status_code != 200:
            print(f"   ❌ Blocked by Eventbrite ({response.status_code})")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 2. Extract Events from hidden JSON-LD script (contains ALL data cleanly)
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                # Data can be a list or single object
                items = data if isinstance(data, list) else [data]
                
                for item in items:
                    if item.get("@type") == "Event":
                        # Extract clean data
                        title = item.get("name")
                        image = item.get("image")
                        event_url = item.get("url")
                        desc = item.get("description", "Check official link for details.")
                        
                        # Handle Date
                        start_date = item.get("startDate", "Upcoming")
                        
                        # Store it
                        events.append({
                            "title": title,
                            "description": desc,
                            "date_text": start_date.replace("T", " "),
                            "location": city.title(),
                            "city": city.title(),
                            "image_url": image,
                            "category": category.title(),
                            "source_type": "external",
                            "external_url": event_url,
                            "price": "Check Link",
                            "is_free": False
                        })
            except:
                continue

    except Exception as e:
        print(f"   ❌ Error scraping Eventbrite: {e}")

    print(f"   ✅ Found {len(events)} events on Eventbrite.")
    return events

def scrape_meetup(city="new-york", category="business"):
    """
    Scrapes Meetup.com search page using JSON-LD extraction.
    """
    print(f"   Searching Meetup in {city} for {category}...")
    events = []
    
    # Meetup Search URL (Generic US search for demo)
    url = f"https://www.meetup.com/find/?keywords={category}&location=us--{city[0:2]}--{city}"
    
    try:
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Meetup also uses JSON-LD
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                # Meetup usually puts the list inside 'itemListElement'
                if "itemListElement" in data:
                    for entry in data["itemListElement"]:
                        item = entry.get("item", {})
                        if item.get("@type") == "Event":
                            events.append({
                                "title": item.get("name"),
                                "description": item.get("description", "Networking event on Meetup."),
                                "date_text": item.get("startDate", "Upcoming").replace("T", " "),
                                "location": item.get("location", {}).get("name", city.title()),
                                "city": city.title(),
                                "image_url": item.get("image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7"),
                                "category": category.title(),
                                "source_type": "external",
                                "external_url": item.get("url"),
                                "price": "Check Link",
                                "is_free": False
                            })
            except:
                continue
                
    except Exception as e:
        print(f"   ❌ Error scraping Meetup: {e}")

    print(f"   ✅ Found {len(events)} events on Meetup.")
    return events

# Main Aggregator
def get_combined_events():
    all_data = []
    # Demo cities
    cities = ["san-francisco", "new-york", "london"]
    
    for city in cities:
        # 1. Get Eventbrite
        eb_events = scrape_eventbrite(city, "business")
        all_data.extend(eb_events)
        time.sleep(2) # Sleep to avoid blocking
        
        # 2. Get Meetup
        mu_events = scrape_meetup(city, "tech")
        all_data.extend(mu_events)
        time.sleep(2)

    return all_data