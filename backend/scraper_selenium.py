from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def setup_driver():
    """
    Sets up a Chrome browser in HEADLESS (Invisible) mode.
    """
    chrome_options = Options()
    
    # ✅ THIS IS THE KEY LINE. Keep it active!
    chrome_options.add_argument("--headless=new") 
    
    # These lines help bypass detection even in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_eventbrite_selenium(city="san-francisco", category="business"):
    print(f"   Searching Eventbrite (via Selenium) in {city}...")
    events = []
    driver = setup_driver()
    
    try:
        url = f"https://www.eventbrite.com/d/ca--{city}/{category}--events/"
        driver.get(url)
        
        # Wait for Eventbrite's heavy React to load
        time.sleep(5) 
        
        # Now pass the fully loaded HTML to BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract JSON-LD (Same strategy as before, but now the data is actually there!)
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if item.get("@type") == "Event":
                        events.append({
                            "title": item.get("name"),
                            "description": item.get("description", "Eventbrite Event"),
                            "date_text": item.get("startDate", "Upcoming").replace("T", " "),
                            "location": city.title(),
                            "city": city.title(),
                            "image_url": item.get("image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7"),
                            "category": category.title(),
                            "source_type": "external",
                            "external_url": item.get("url"),
                            "price": "Check Link",
                            "is_free": False
                        })
            except: continue
            
    except Exception as e:
        print(f"   ❌ Selenium Error: {e}")
    finally:
        driver.quit() # Close the browser

    print(f"   ✅ Found {len(events)} events on Eventbrite.")
    return events

def scrape_meetup_selenium(city="new-york", category="tech"):
    print(f"   Searching Meetup (via Selenium) in {city}...")
    events = []
    driver = setup_driver()
    
    try:
        url = f"https://www.meetup.com/find/?keywords={category}&location=us--{city[0:2]}--{city}"
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Meetup JSON-LD extraction
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
                                "location": city.title(),
                                "city": city.title(),
                                "image_url": item.get("image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7"),
                                "category": category.title(),
                                "source_type": "external",
                                "external_url": item.get("url"),
                                "price": "Check Link",
                                "is_free": False
                            })
            except: continue

    except Exception as e:
        print(f"   ❌ Selenium Error: {e}")
    finally:
        driver.quit()

    print(f"   ✅ Found {len(events)} events on Meetup.")
    return events

# Combined Scraper Function
def get_selenium_events():
    all_data = []
    # Using just one city for test speed, add more later
    cities = ["new-york", "london"] 
    
    for city in cities:
        all_data.extend(scrape_eventbrite_selenium(city, "business"))
        all_data.extend(scrape_meetup_selenium(city, "tech"))
        
    return all_data