
import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, MapPin, Tag, ExternalLink, Zap } from 'lucide-react';
import { Event } from '../types';

interface EventCardProps {
  event: Event;
}

const EventCard: React.FC<EventCardProps> = ({ event }) => {
  return (
    <div className="glass group rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-white/40">
      <div className="relative h-48 overflow-hidden">
        <img 
          src={event.image_url} 
          alt={event.title}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        />
        <div className="absolute top-4 right-4 flex gap-2">
          {event.is_free && (
            <span className="bg-green-500 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider shadow-sm">
              Free
            </span>
          )}
          <span className="bg-[#6D28D9]/80 backdrop-blur text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider shadow-sm">
            {event.category}
          </span>
        </div>
        <div className="absolute bottom-4 left-4">
           <span className="bg-black/60 backdrop-blur text-white text-[10px] font-medium px-2 py-1 rounded-lg flex items-center gap-1">
             <MapPin className="w-3 h-3" /> {event.city}
           </span>
        </div>
      </div>

      <div className="p-5">
        <div className="flex items-center gap-2 text-[#8B5CF6] text-xs font-semibold mb-2">
          <Calendar className="w-3 h-3" />
          {event.date_text.split('-')[0]}
        </div>
        
        <h3 className="text-gray-900 font-bold text-lg mb-2 line-clamp-1 leading-tight group-hover:text-[#6D28D9] transition-colors">
          {event.title}
        </h3>
        
        <p className="text-gray-500 text-sm mb-4 line-clamp-2 leading-relaxed h-10">
          {event.description}
        </p>

        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
          <Link 
            to={`/events/${event.id}`}
            className="text-[#6D28D9] text-sm font-bold flex items-center gap-1 hover:gap-2 transition-all"
          >
            View Details 
            <ExternalLink className="w-3 h-3" />
          </Link>
          
          <div className="flex items-center gap-1 text-gray-400 text-[10px] uppercase font-bold tracking-widest">
            {event.source_type === 'external' ? 'Partner Site' : 'Official Host'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
