import React from 'react';
import { Calendar, MapPin, ExternalLink } from 'lucide-react';

// Note: Ensure this path matches where your types file is located
// If you don't have a types file, you can remove the interface part below
import { Event } from '../types';

interface EventCardProps {
  event: Event;
}

const EventCard: React.FC<EventCardProps> = ({ event }) => {
  return (
    /* ✅ 1. THE WHOLE CARD IS NOW A LINK (<a>) */
    <a 
      href={event.external_url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="glass group rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-white/40 block h-full cursor-pointer"
    >
      {/* Image Section */}
      <div className="relative h-48 overflow-hidden">
        <img 
          src={event.image_url} 
          alt={event.title}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        />
        
        {/* Badges (Free + Category) */}
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

        {/* Location Badge */}
        <div className="absolute bottom-4 left-4">
           <span className="bg-black/60 backdrop-blur text-white text-[10px] font-medium px-2 py-1 rounded-lg flex items-center gap-1">
             <MapPin className="w-3 h-3" /> {event.city}
           </span>
        </div>
      </div>

      {/* Content Section */}
      <div className="p-5">
        {/* Date */}
        <div className="flex items-center gap-2 text-[#8B5CF6] text-xs font-semibold mb-2">
          <Calendar className="w-3 h-3" />
          {event.date_text.split('-')[0]}
        </div>
        
        {/* Title */}
        <h3 className="text-gray-900 font-bold text-lg mb-2 line-clamp-1 leading-tight group-hover:text-[#6D28D9] transition-colors">
          {event.title}
        </h3>
        
        {/* Description */}
        <p className="text-gray-500 text-sm mb-4 line-clamp-2 leading-relaxed h-10">
          {event.description}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
          {/* ✅ 2. "View Details" is now just visual text (since parent is the link) */}
          <span className="text-[#6D28D9] text-sm font-bold flex items-center gap-1 group-hover:gap-2 transition-all">
            View Details 
            <ExternalLink className="w-3 h-3" />
          </span>
          
          <div className="flex items-center gap-1 text-gray-400 text-[10px] uppercase font-bold tracking-widest">
            {event.source_type === 'external' ? 'Partner Site' : 'Official Host'}
          </div>
        </div>
      </div>
    </a>
  );
};

export default EventCard;