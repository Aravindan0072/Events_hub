import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Lock, Loader2, ArrowRight } from 'lucide-react';

const Signup: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      login({
        id: Date.now().toString(),
        name: name,
        email: email,
      });
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="glass w-full max-w-md p-8 rounded-2xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#7C3AED] to-[#6D28D9]" />

        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Create Account</h2>
          <p className="text-gray-500">Join EventFlow today</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
            <div className="relative">
              <User className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9]/20 focus:border-[#6D28D9] outline-none transition-all"
                placeholder="John Doe"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9]/20 focus:border-[#6D28D9] outline-none transition-all"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#6D28D9]/20 focus:border-[#6D28D9] outline-none transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-[#6D28D9] hover:bg-[#5b21b6] text-white font-bold py-3 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-70 mt-2 shadow-lg shadow-purple-200"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Get Started <ArrowRight className="w-5 h-5" /></>}
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-gray-500">
          Already have an account?{' '}
          <Link to="/login" className="text-[#6D28D9] font-bold hover:underline">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;