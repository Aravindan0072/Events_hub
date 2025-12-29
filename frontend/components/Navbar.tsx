import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Calendar, LayoutDashboard, LogOut, Menu, X } from 'lucide-react'; // Added Menu and X icons

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsMobileMenuOpen(false); // Close menu on logout
  };

  const toggleMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

  return (
    <nav className="purple-gradient text-white shadow-lg sticky top-0 z-50 h-16">
      <div className="container mx-auto px-4 h-full flex justify-between items-center">
        {/* Logo Section */}
        <Link to="/" className="flex items-center gap-2 font-bold text-xl tracking-tight z-50">
          <div className="bg-white p-1 rounded-lg">
            <Calendar className="text-[#6D28D9] w-6 h-6" />
          </div>
          EventFlow
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-6">
          <Link to="/" className="hover:text-purple-200 transition-colors font-medium">Events</Link>
          <Link to="/dashboard" className="hover:text-purple-200 transition-colors font-medium">Dashboard</Link>
        </div>

        {/* Desktop Auth Section */}
        <div className="hidden md:flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <div 
                className="flex items-center gap-2 group cursor-pointer hover:bg-white/10 px-2 py-1 rounded-lg transition-all" 
                onClick={() => navigate('/dashboard')}
                role="button"
                tabIndex={0}
              >
                <img 
                  src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.name || 'User'}`} 
                  alt="avatar" 
                  className="w-8 h-8 rounded-full border-2 border-white/50 bg-white"
                />
                <span className="font-medium text-sm">{user?.name}</span>
              </div>
              <button 
                onClick={handleLogout}
                className="p-2 hover:bg-white/20 rounded-full transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className="px-4 py-2 hover:bg-white/10 rounded-lg transition-colors text-sm font-medium">Login</Link>
              <Link to="/signup" className="px-4 py-2 bg-white text-[#6D28D9] rounded-lg shadow-md hover:bg-gray-100 transition-colors text-sm font-bold">Sign Up</Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Toggle Button */}
        <button 
          className="md:hidden p-2 z-50 focus:outline-none" 
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMobileMenuOpen && (
        <div className="absolute top-16 left-0 w-full bg-[#5b21b6] md:hidden shadow-xl border-t border-white/10 animate-fade-in-down">
          <div className="flex flex-col p-4 space-y-4">
            <Link 
              to="/" 
              className="flex items-center gap-2 text-lg font-medium hover:bg-white/10 p-2 rounded-lg"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              <Calendar className="w-5 h-5" /> Events
            </Link>
            <Link 
              to="/dashboard" 
              className="flex items-center gap-2 text-lg font-medium hover:bg-white/10 p-2 rounded-lg"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              <LayoutDashboard className="w-5 h-5" /> Dashboard
            </Link>
            
            <div className="h-px bg-white/20 my-2" />

            {isAuthenticated ? (
              <div className="space-y-4">
                 <div className="flex items-center gap-3 p-2 bg-white/10 rounded-lg">
                    <img 
                      src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.name || 'User'}`} 
                      alt="avatar" 
                      className="w-8 h-8 rounded-full border border-white"
                    />
                    <span className="font-medium">{user?.name}</span>
                 </div>
                 <button 
                  onClick={handleLogout}
                  className="w-full flex items-center gap-2 bg-red-500/80 hover:bg-red-500 p-2 rounded-lg transition-colors text-left"
                 >
                   <LogOut className="w-5 h-5" /> Logout
                 </button>
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                <Link 
                  to="/login" 
                  className="text-center px-4 py-2 hover:bg-white/10 rounded-lg border border-white/20"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link 
                  to="/signup" 
                  className="text-center px-4 py-2 bg-white text-[#6D28D9] rounded-lg font-bold"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;