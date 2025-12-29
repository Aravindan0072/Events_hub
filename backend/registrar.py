import requests
import json

# YOUR API KEY
API_TOKEN = "UESCKVBWXSGMLNR5DYXP"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_free_ticket_class(event_id):
    print(f"🔍 API SCOUT: Checking tickets for Event {event_id}...")
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"
    
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        if response.status_code != 200:
            print(f"❌ API Error: {data}")
            return None

        ticket_classes = data.get("ticket_classes", [])
        
        for ticket in ticket_classes:
            # Find the FREE ticket that is AVAILABLE
            if ticket.get("free") and ticket.get("on_sale_status") == "AVAILABLE":
                print(f"✅ Found Free Ticket ID: {ticket['id']}")
                return ticket['id']
                
        print("⚠️ No free tickets found.")
        return None

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def register_for_event(event_id):
    print(f"🔌 API AGENT: Processing Registration for {event_id}...")
    
    # 1. Get Ticket ID
    ticket_id = get_free_ticket_class(event_id)
    if not ticket_id:
        return {"status": "failed", "message": "No valid free ticket found (or event is paid)."}

    # 2. Place Order
    url = "https://www.eventbriteapi.com/v3/orders/"
    payload = {
        "event_id": str(event_id),
        "ticket_class_id": ticket_id,
        "quantity": 1
    }
    
    print("🚀 Sending Order Command...")
    response = requests.post(url, headers=HEADERS, json=payload)
    
    # DEBUG: Print response
    print(f"📡 Response Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        return {"status": "success", "order": response.json()}
    else:
        # If this fails, it is likely a permission issue
        return {"status": "failed", "message": f"Eventbrite refused: {response.text}"}