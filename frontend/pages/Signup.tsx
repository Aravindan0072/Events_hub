
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Calendar, Mail, Lock, User, CheckCircle } from 'lucide-react';

const Signup: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [agreed, setAgreed] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!agreed) return;
    signup(formData.name, formData.email);
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex bg-gray-50">
      <div className="hidden lg:flex flex-1 purple-gradient p-12 flex-col justify-between text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -ml-32 -mb-32 w-96 h-96 bg-black/10 rounded-full blur-3xl"></div>
        <div className="relative">
          <Link to="/" className="flex items-center gap-2 font-bold text-2xl tracking-tight">
            <div className="bg-white p-2 rounded-xl shadow-lg">
              <Calendar className="text-[#6D28D9] w-7 h-7" />
            </div>
            EventFlow
          </Link>
        </div>
        <div className="relative">
          <h1 className="text-5xl font-extrabold mb-6 leading-tight">Start Your Networking Journey</h1>
          <p className="text-xl text-purple-100 max-w-lg leading-relaxed">Create an account to unlock one-click registrations and personalized event feeds.</p>
        </div>
        <div className="text-sm opacity-60">© 2024 EventFlow Aggregator. All rights reserved.</div>
      </div>

      <div className="flex-1 flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md">
          <div className="mb-10">
            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">Create Account</h2>
            <p className="text-gray-500 font-medium">Join 500+ professionals in Chennai.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-2 gap-2 p-1 bg-gray-100 rounded-xl mb-8">
              <Link to="/login" className="py-2 text-center text-sm font-semibold text-gray-500 hover:text-gray-700">Log In</Link>
              <Link to="/signup" className="py-2 text-center text-sm font-bold rounded-lg bg-white shadow-sm text-gray-900">Sign Up</Link>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-1">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input 
                    type="text" required placeholder="Arjun Reddy"
                    className="w-full pl-11 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-700 mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input 
                    type="email" required placeholder="name@example.com"
                    className="w-full pl-11 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-1">Password</label>
                  <input 
                    type="password" required placeholder="••••••••"
                    className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-1">Confirm</label>
                  <input 
                    type="password" required placeholder="••••••••"
                    className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                  />
                </div>
              </div>
            </div>

            <div className="flex items-start gap-3 py-2">
              <input 
                type="checkbox" 
                id="agreed"
                className="mt-1 w-4 h-4 rounded border-gray-300 text-[#6D28D9] focus:ring-[#6D28D9]"
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
              />
              <label htmlFor="agreed" className="text-sm text-gray-500 leading-snug">
                I agree to the <a href="#" className="text-[#8B5CF6] font-bold hover:underline">Privacy Policy</a> and <a href="#" className="text-[#8B5CF6] font-bold hover:underline">Terms & Conditions</a>
              </label>
            </div>

            <button 
              type="submit"
              disabled={!agreed}
              className={`w-full py-4 rounded-xl font-bold shadow-lg transition-all ${
                agreed 
                  ? 'purple-gradient text-white shadow-purple-200 hover:shadow-purple-300 active:scale-[0.98]' 
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none'
              }`}
            >
              Sign Up
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Signup;
