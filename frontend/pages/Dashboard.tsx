import React, { useState, useEffect } from 'react';
import EventCard from '../components/EventCard';
import { Search, Loader2, RefreshCw } from 'lucide-react';
import { Event } from '../types';

// Updated Categories for Professional Focus
const CATEGORIES = ['All', 'Technology', 'Business', 'Startup', 'AI & Data', 'Career'];

const Dashboard: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [isRefreshing, setIsRefreshing] = useState(false);

  // 1. Function to Fetch Events from Python Backend
  const fetchEvents = async () => {
    try {
      setIsLoading(true);
      // Fetches from your running FastAPI server
      const response = await fetch('http://localhost:8000/api/events');
      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error("Failed to fetch events:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 2. Load events when page opens
  useEffect(() => {
    fetchEvents();
  }, []);

  // 3. Button to Trigger Python Scraper
  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await fetch('http://localhost:8000/api/refresh-events', { method: 'POST' });
      await fetchEvents(); // Reload list after scraping
    } catch (error) {
      console.error("Scrape failed:", error);
    } finally {
      setIsRefreshing(false);
    }
  };

  // 4. Filtering Logic (Frontend Side)
  const filteredEvents = events.filter((event) => {
    const matchesCategory = selectedCategory === 'All' || event.category === selectedCategory;
    const matchesSearch = 
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      (event.city && event.city.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gray-50 pb-12">
      {/* Header / Search Section */}
      <div className="bg-white border-b sticky top-16 z-30 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Discover Events</h1>
              <p className="text-gray-500 mt-1">
                Real-time events from around the globe.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
               {/* Search Bar */}
              <div className="relative w-full md:w-80 group">
                <input 
                  type="text"
                  placeholder="Search events or cities..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-[#6D28D9]/20 focus:border-[#6D28D9] outline-none transition-all"
                />
                <Search className="absolute left-4 top-3.5 text-gray-400 group-focus-within:text-[#6D28D9] w-5 h-5 transition-colors" />
              </div>

              {/* Refresh Scraper Button */}
              <button 
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="p-3 bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-colors disabled:opacity-50"
                title="Scrape New Events"
              >
                <RefreshCw className={`w-5 h-5 ${isRefreshing ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
          
          {/* Category Pills */}
          <div className="flex items-center gap-3 mt-8 overflow-x-auto pb-2 scrollbar-hide">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-5 py-2 rounded-full text-sm font-semibold whitespace-nowrap transition-all duration-200 ${
                  selectedCategory === cat 
                    ? 'bg-[#6D28D9] text-white shadow-md shadow-purple-200 transform scale-105' 
                    : 'bg-white border border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="container mx-auto px-4 py-8">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="w-10 h-10 text-[#6D28D9] animate-spin mb-4" />
            <p className="text-gray-500">Loading live events...</p>
          </div>
        ) : filteredEvents.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredEvents.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="bg-purple-50 p-6 rounded-full mb-4">
              <Search className="text-[#6D28D9] w-10 h-10" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">No events found</h3>
            <p className="text-gray-500 mt-2 max-w-md">
              Try clicking the refresh button to scrape new data.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;