import requests
from bs4 import BeautifulSoup
import time
import json
import random

def get_real_events(city_list=["chennai", "bangalore", "new-york", "london", "singapore", "dubai"]):
    """
    DEEP SCRAPER: Visits every event link to get REAL description and REAL image.
    """
    all_events = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    print(f"🌍 Starting DEEP Scrape (Real Images & Descriptions)...")

    for city in city_list:
        city_slug = city.replace(" ", "-").lower()
        url = f"https://allevents.in/{city_slug}/business"
        
        try:
            print(f"🔍 Searching {city.upper()}...")
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find event cards
            event_items = soup.find_all("li", attrs={"data-link": True}) 
            if not event_items:
                 event_items = soup.select('div.event-card') 

            city_count = 0
            
            # Limit to 5 events per city to keep it fast enough (Deep scraping takes time)
            for item in event_items[:5]: 
                try:
                    # 1. Get the Link
                    link = item.get("data-link") or item.find("a")['href']
                    if not link: continue
                    
                    # 2. VISIT THE DETAILS PAGE (The fix for missing data)
                    # print(f"   ...fetching details: {link}")
                    detail_response = requests.get(link, headers=headers, timeout=10)
                    detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                    # 3. Extract Real JSON-LD Data (Best source for clean data)
                    structured_data = detail_soup.find('script', type='application/ld+json')
                    
                    real_title = "Unknown Event"
                    real_desc = "No description available."
                    real_image = None
                    real_location = city.title()
                    
                    if structured_data:
                        data = json.loads(structured_data.string)
                        real_title = data.get('name', real_title)
                        real_desc = data.get('description', real_desc)
                        real_image = data.get('image', None)
                        
                        # Handle location object
                        loc = data.get('location', {})
                        if isinstance(loc, dict):
                            real_location = loc.get('name', real_location)

                    # 4. Fallback if JSON-LD fails (Scrape HTML tags)
                    if real_image is None:
                        # Try finding the main banner
                        banner = detail_soup.find("img", class_="event-banner-image")
                        if banner: real_image = banner.get("src")
                    
                    if "No description" in real_desc:
                        # Try finding the description div
                        desc_div = detail_soup.find("div", class_="event-description-html")
                        if desc_div: real_desc = desc_div.get_text(strip=True)[:500] + "..."

                    # 5. Clean up the data
                    if not real_image:
                        # Only use fallback if absolutely necessary
                        real_image = "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=800"

                    event_obj = {
                        "title": real_title,
                        "description": real_desc, # NOW CONTAINS REAL TEXT
                        "date_text": "Check Link", # JSON dates are hard to format, keeping simple
                        "location": real_location,
                        "image_url": real_image,   # NOW CONTAINS REAL IMAGE
                        "source_type": "external",
                        "external_url": link,
                        "is_free": False,
                        "category": "Business"
                    }

                    if event_obj not in all_events:
                        all_events.append(event_obj)
                        city_count += 1
                        print(f"      -> Got: {real_title[:30]}...")
                
                except Exception as e:
                    continue 
                
                # Sleep to prevent blocking
                time.sleep(0.5)

            print(f"   ✅ Processed {city_count} events for {city}")

        except Exception as e:
            print(f"   ❌ Error scraping {city}: {e}")

    return all_events