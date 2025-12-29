from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 1. Reset Database
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("🌱 Seeding Database with 20 Dummy Events...")

events_data = [
    # --- EXTERNAL EVENTS (10) ---
    {
        "title": "Chennai AI Summit 2025",
        "description": "Join the leading minds in AI for a day of talks and networking.",
        "date": "2025-10-15T09:00:00",
        "location": "Chennai Trade Centre",
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e",
        "category": "Tech",
        "is_free": False,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "SaaS Founders Meetup",
        "description": "A casual meetup for SaaS founders to share metrics and coffee.",
        "date": "2025-10-20T18:00:00",
        "location": "T-Nagar, Chennai",
        "image_url": "https://images.unsplash.com/photo-1515187029135-18ee286d815b",
        "category": "Startup",
        "is_free": True,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "Global FinTech Conference",
        "description": "Explore the future of finance and blockchain technology.",
        "date": "2025-11-05T10:00:00",
        "location": "ITC Grand Chola",
        "image_url": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7",
        "category": "Finance",
        "is_free": False,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "React Native Workshop",
        "description": "Deep dive into mobile app development with React Native.",
        "date": "2025-10-25T14:00:00",
        "location": "Anna University",
        "image_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee",
        "category": "Tech",
        "is_free": True,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "Digital Marketing Bootcamp",
        "description": "Master SEO, SEM, and Social Media Marketing in 2 days.",
        "date": "2025-11-10T09:30:00",
        "location": "OMR, Chennai",
        "image_url": "https://images.unsplash.com/photo-1533750516457-a7f992034fec",
        "category": "Marketing",
        "is_free": False,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
     {
        "title": "Cloud Computing Expo",
        "description": "AWS, Azure, and Google Cloud experts under one roof.",
        "date": "2025-12-01T09:00:00",
        "location": "Bangalore Convention Center",
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
        "category": "Tech",
        "is_free": False,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "Women in Tech Gathering",
        "description": "Empowering women leaders in the technology sector.",
        "date": "2025-10-30T17:00:00",
        "location": "WeWork Galaxy",
        "image_url": "https://images.unsplash.com/photo-1573164713988-8665fc963095",
        "category": "Tech",
        "is_free": True,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "Blockchain Developers Night",
        "description": "Coding session and networking for Web3 enthusiasts.",
        "date": "2025-11-15T19:00:00",
        "location": "Cyber City Hub",
        "image_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0",
        "category": "Tech",
        "is_free": True,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "UX/UI Design Sprint",
        "description": "A rapid prototyping workshop for designers.",
        "date": "2025-11-20T10:00:00",
        "location": "Design Cafe",
        "image_url": "https://images.unsplash.com/photo-1586717791821-3f44a5638d0f",
        "category": "Design",
        "is_free": False,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },
    {
        "title": "Startup Pitch Night",
        "description": "Watch 10 startups pitch to top VCs.",
        "date": "2025-12-05T18:30:00",
        "location": "The Hive",
        "image_url": "https://images.unsplash.com/photo-1559136555-9303baea8ebd",
        "category": "Startup",
        "is_free": True,
        "source_type": "external",
        "external_url": "https://www.google.com/search?q=google.com"
    },

    # --- INTERNAL EVENTS (10) ---
    {
        "title": "Local Python Study Group",
        "description": "Weekly study group for Python enthusiasts.",
        "date": "2025-10-18T16:00:00",
        "location": "Library Hall A",
        "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935",
        "category": "Education",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Charity Run 2025",
        "description": "5K run to support local schools.",
        "date": "2025-11-02T06:00:00",
        "location": "Marina Beach",
        "image_url": "https://images.unsplash.com/photo-1552674605-469523fbaf4d",
        "category": "Health",
        "is_free": False,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Indie Music Jam",
        "description": "Open mic night for independent musicians.",
        "date": "2025-10-22T20:00:00",
        "location": "The Garage Cafe",
        "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4",
        "category": "Arts",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Photography Walk",
        "description": "Explore the city architecture through your lens.",
        "date": "2025-11-08T07:00:00",
        "location": "Mylapore",
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32",
        "category": "Arts",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Yoga in the Park",
        "description": "Morning yoga session for all levels.",
        "date": "2025-10-28T06:30:00",
        "location": "Semmozhi Poonga",
        "image_url": "https://images.unsplash.com/photo-1544367563-12123d8965cd",
        "category": "Health",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Book Club Monthly",
        "description": "Discussing 'Atomic Habits' this month.",
        "date": "2025-11-12T17:00:00",
        "location": "City Library",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6",
        "category": "Education",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Weekend Coding Bootcamp",
        "description": "Intensive coding session for beginners.",
        "date": "2025-11-22T09:00:00",
        "location": "Tech Hub",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97",
        "category": "Education",
        "is_free": False,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Art Exhibition Opening",
        "description": "Showcasing local artists' new collections.",
        "date": "2025-12-10T18:00:00",
        "location": "Modern Art Gallery",
        "image_url": "https://images.unsplash.com/photo-1518998053901-5348d3969105",
        "category": "Arts",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Community Clean-up",
        "description": "Join us to keep our neighborhood clean.",
        "date": "2025-10-26T08:00:00",
        "location": "Besant Nagar Beach",
        "image_url": "https://images.unsplash.com/photo-1618477461853-586eff3f7280",
        "category": "Community",
        "is_free": True,
        "source_type": "internal",
        "external_url": None
    },
    {
        "title": "Food Festival 2025",
        "description": "Taste cuisines from around the world.",
        "date": "2025-12-15T12:00:00",
        "location": "Island Grounds",
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1",
        "category": "Food",
        "is_free": False,
        "source_type": "internal",
        "external_url": None
    }
]

for event in events_data:
    db_event = models.Event(**event)
    db.add(db_event)

db.commit()
print("✅ Successfully added 20 Events!")
db.close()