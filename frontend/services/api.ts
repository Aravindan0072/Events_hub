
import { Event } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

// Fallback mock data if server is unreachable
const MOCK_EVENTS: Event[] = [
  {
    id: '1',
    title: 'SaaS Founders Mixer: Chennai Edition',
    description: 'Join the most elite circle of SaaS founders in Chennai for an evening of networking and insights.',
    date_text: 'Oct 24, 4:00 PM - 7:00 PM',
    location: 'IIT Madras Research Park, Taranami, Chennai',
    image_url: 'https://picsum.photos/seed/saas/800/600',
    category: 'Startup',
    city: 'Chennai',
    is_free: true,
    source_type: 'external',
    external_url: 'https://eventbrite.com/example-saas-mixer',
    views: 1240,
    clicks: 450
  },
  {
    id: '2',
    title: 'React India: Advanced Patterns Workshop',
    description: 'Master advanced React patterns, performance optimization, and architectural decisions.',
    date_text: 'Aug 12, 10:00 AM - 2:00 PM',
    location: 'The Hive, OMR, Chennai',
    image_url: 'https://picsum.photos/seed/react/800/600',
    category: 'Workshop',
    city: 'Chennai',
    is_free: false,
    source_type: 'internal',
    views: 890,
    clicks: 120
  },
  {
    id: '3',
    title: 'Bangalore Tech Summit 2024',
    description: 'The biggest tech summit in Bangalore featuring global speakers and innovators.',
    date_text: 'Nov 15, 9:00 AM - 6:00 PM',
    location: 'BIEC, Bangalore',
    image_url: 'https://picsum.photos/seed/tech/800/600',
    category: 'Conference',
    city: 'Bangalore',
    is_free: false,
    source_type: 'external',
    external_url: 'https://bangaloretechsummit.com',
    views: 3500,
    clicks: 1100
  }
];

export const fetchEvents = async (): Promise<Event[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/events`);
    if (!response.ok) throw new Error('API unreachable');
    return await response.json();
  } catch (error) {
    console.warn('Backend not available, using mock data.');
    return MOCK_EVENTS;
  }
};

export const fetchEventById = async (id: string): Promise<Event | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}/events/${id}`);
    if (!response.ok) throw new Error('API unreachable');
    return await response.json();
  } catch (error) {
    console.warn('Backend not available, using mock data.');
    return MOCK_EVENTS.find(e => e.id === id) || null;
  }
};

export const trackClick = async (id: string): Promise<void> => {
  try {
    await fetch(`${API_BASE_URL}/analytics/click/${id}`, { method: 'POST' });
  } catch (error) {
    console.warn('Failed to track click analytics');
  }
};
