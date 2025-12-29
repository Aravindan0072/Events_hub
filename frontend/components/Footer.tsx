import React from 'react';
import { Calendar, Github, Twitter, Linkedin, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white py-12 border-t border-gray-800 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 font-bold text-xl mb-4">
              <div className="bg-white p-1 rounded-lg">
                <Calendar className="text-[#6D28D9] w-5 h-5" />
              </div>
              EventFlow
            </div>
            <p className="text-gray-400 text-sm leading-relaxed max-w-xs">
              Discover, track, and attend the best events in your city. 
              The ultimate platform for event enthusiasts and organizers.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-bold mb-4 text-gray-200">Platform</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link to="/" className="hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
              <li><Link to="/login" className="hover:text-white transition-colors">Login</Link></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold mb-4 text-gray-200">Connect</h4>
            <div className="flex gap-4">
              <a href="#" className="bg-gray-800 p-2 rounded-lg hover:bg-[#6D28D9] transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="bg-gray-800 p-2 rounded-lg hover:bg-[#6D28D9] transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="bg-gray-800 p-2 rounded-lg hover:bg-[#6D28D9] transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
          <p>&copy; 2025 EventFlow. All rights reserved.</p>
          <div className="flex items-center gap-1 mt-2 md:mt-0">
            Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> by You
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;