import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Calendar, MapPin, Share2, ArrowLeft, Heart, Globe, Ticket, Loader2 } from 'lucide-react';
import { Event } from '../types';

const EventDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchEventDetail = async () => {
      try {
        setLoading(true);
        // Fetch from real Python Backend
        const response = await fetch(`http://localhost:8000/api/events/${id}`);
        
        if (!response.ok) {
          throw new Error('Event not found');
        }
        
        const data = await response.json();
        setEvent(data);
      } catch (err) {
        console.error("Error fetching event:", err);
        setError('Failed to load event details.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchEventDetail();
    }
  }, [id]);

  const handleTicketClick = () => {
    // 1. (Optional) Track click in backend
    // fetch(`http://localhost:8000/api/analytics/click/${id}`, { method: 'POST' });

    // 2. Open external link
    if (event?.external_url) {
      window.open(event.external_url, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-[#6D28D9] animate-spin" />
      </div>
    );
  }

  if (error || !event) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-center p-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Event not found</h2>
        <p className="text-gray-500 mb-4">{error || "The event you are looking for doesn't exist."}</p>
        <Link to="/dashboard" className="px-6 py-2 bg-[#6D28D9] text-white rounded-lg hover:bg-[#5b21b6] transition-colors">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-20">
      {/* Hero Image Section */}
      <div className="relative h-[400px] w-full group">
        <img 
          src={event.image_url || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87'} 
          alt={event.title} 
          className="w-full h-full object-cover" 
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
        
        <div className="absolute top-6 left-4 md:left-8">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center gap-2 text-white/90 hover:text-white bg-black/30 backdrop-blur-md px-4 py-2 rounded-full transition-all hover:bg-black/50"
          >
            <ArrowLeft className="w-4 h-4" /> Back
          </button>
        </div>
      </div>

      {/* Content Container */}
      <div className="container mx-auto px-4 -mt-32 relative z-10">
        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* Main Info Card */}
          <div className="flex-1 bg-white rounded-2xl shadow-xl border border-gray-100 p-6 md:p-8">
            <div className="flex justify-between items-start mb-6">
              <span className="bg-[#6D28D9]/10 text-[#6D28D9] font-bold px-3 py-1 rounded-full text-sm uppercase tracking-wide">
                {event.category}
              </span>
              <div className="flex gap-3">
                <button className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors">
                  <Heart className="w-6 h-6" />
                </button>
                <button className="p-2 text-gray-400 hover:text-blue-500 hover:bg-blue-50 rounded-full transition-colors">
                  <Share2 className="w-6 h-6" />
                </button>
              </div>
            </div>

            <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4 leading-tight">
              {event.title}
            </h1>

            <div className="flex flex-col gap-4 border-b border-gray-100 pb-8 mb-8">
              <div className="flex items-center gap-3 text-gray-600">
                <div className="bg-purple-50 p-2 rounded-lg">
                  <Calendar className="w-6 h-6 text-[#6D28D9]" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">Date & Time</p>
                  <p className="text-sm">{event.date_text}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3 text-gray-600">
                <div className="bg-purple-50 p-2 rounded-lg">
                  <MapPin className="w-6 h-6 text-[#6D28D9]" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">Location</p>
                  <p className="text-sm">{event.location}</p>
                </div>
              </div>

               {/* View Count Badge (New Feature) */}
               <div className="flex items-center gap-2 text-xs text-gray-400 mt-2">
                 <span className="bg-gray-100 px-2 py-1 rounded">👀 {event.views || 0} people viewed this</span>
               </div>
            </div>

            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">About this Event</h3>
              <p className="text-gray-600 leading-relaxed whitespace-pre-line">
                {event.description}
              </p>
            </div>
          </div>

          {/* Sidebar / Ticket Card */}
          <div className="lg:w-96">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 sticky top-24">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Tickets & Info</h3>
              
              <div className="flex justify-between items-center mb-6">
                <span className="text-gray-500">Price</span>
                <span className="text-2xl font-bold text-[#6D28D9]">{event.price || 'Check Link'}</span>
              </div>

              <button 
                onClick={handleTicketClick}
                className="w-full bg-[#6D28D9] hover:bg-[#5b21b6] text-white font-bold py-4 rounded-xl shadow-lg shadow-purple-200 transition-all flex items-center justify-center gap-2 mb-4"
              >
                <Ticket className="w-5 h-5" />
                {event.source_type === 'external' ? 'Get Tickets on Partner Site' : 'Get Tickets Now'}
              </button>

              {event.source_type === 'external' && (
                <div className="text-center">
                  <p className="text-xs text-gray-400 mb-2">
                    This event is hosted by an external partner.
                  </p>
                  {event.external_url && (
                    <a 
                      href={event.external_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-[#6D28D9] font-semibold flex items-center justify-center gap-1 hover:underline"
                    >
                      Visit Official Website <Globe className="w-3 h-3" />
                    </a>
                  )}
                </div>
              )}
              
              <div className="mt-6 pt-6 border-t border-gray-100">
                <p className="text-xs text-center text-gray-400">
                  EventFlow ensures secure booking and verified event details.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default EventDetail;