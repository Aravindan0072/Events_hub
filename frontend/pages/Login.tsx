
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Calendar, Mail, Lock, Eye, EyeOff, CheckCircle } from 'lucide-react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email, password);
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Left side - Brand/Hero */}
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
          <h1 className="text-5xl font-extrabold mb-6 leading-tight">
            Discover Chennai's Best Tech Meetups
          </h1>
          <p className="text-xl text-purple-100 max-w-lg leading-relaxed">
            Join the fastest growing network of professionals. Auto-register for events, track your attendance, and grow your career.
          </p>
          <div className="mt-12 flex items-center gap-2 bg-white/20 backdrop-blur-md w-fit px-4 py-2 rounded-full border border-white/30">
            <CheckCircle className="w-5 h-5 text-green-400" />
            <span className="text-sm font-medium">Trusted by 10,000+ Developers in India</span>
          </div>
        </div>

        <div className="text-sm opacity-60">
          © 2024 EventFlow Aggregator. All rights reserved.
        </div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md">
          <div className="mb-10">
            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">Welcome Back</h2>
            <p className="text-gray-500 font-medium">Enter your details to access your dashboard.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-2 p-1 bg-gray-100 rounded-xl mb-8">
              <Link to="/login" className="py-2 text-center text-sm font-bold rounded-lg bg-white shadow-sm text-gray-900">Log In</Link>
              <Link to="/signup" className="py-2 text-center text-sm font-semibold text-gray-500 hover:text-gray-700">Sign Up</Link>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input 
                    type="email" 
                    required 
                    placeholder="name@example.com"
                    className="w-full pl-11 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <label className="block text-sm font-bold text-gray-700">Password</label>
                  <a href="#" className="text-xs font-bold text-[#8B5CF6] hover:underline">Forgot Password?</a>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input 
                    type={showPassword ? "text" : "password"} 
                    required 
                    placeholder="Enter your password"
                    className="w-full pl-11 pr-11 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9] focus:border-transparent transition-all outline-none"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <button 
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </div>

            <button 
              type="submit"
              className="w-full purple-gradient text-white font-bold py-4 rounded-xl shadow-lg shadow-purple-200 hover:shadow-purple-300 transition-all active:scale-[0.98]"
            >
              Sign In
            </button>

            <div className="relative py-4">
              <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200"></div></div>
              <div className="relative flex justify-center text-xs uppercase"><span className="bg-gray-50 px-2 text-gray-500 font-bold tracking-widest">Or continue with</span></div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button type="button" className="flex items-center justify-center gap-2 border border-gray-200 py-3 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-sm">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" className="w-5 h-5" /> Google
              </button>
              <button type="button" className="flex items-center justify-center gap-2 border border-gray-200 py-3 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-sm">
                <img src="https://www.svgrepo.com/show/448234/linkedin.svg" className="w-5 h-5" /> LinkedIn
              </button>
            </div>

            <p className="text-center text-xs text-gray-400">
              By continuing, you agree to our <a href="#" className="underline">Terms of Service</a> and <a href="#" className="underline">Privacy Policy</a>.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
