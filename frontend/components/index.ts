export interface Event {
  id: string;
  title: string;
  description: string;
  date_text: string;     // e.g. "Oct 15, 2025 • 9:00 AM"
  location: string;      // Full address
  city: string;          // e.g. "San Francisco"
  image_url: string;
  category: string;
  price: string;         // Display string like "$299"
  is_free: boolean;
  source_type: 'internal' | 'external';
  organizer?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}