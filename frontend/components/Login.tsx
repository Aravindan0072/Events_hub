 import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, Loader2, ArrowRight } from 'lucide-react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      if (email && password.length >= 6) {
        // Successful login mock
        login({
          id: '1',
          name: email.split('@')[0], // Use part of email as name for now
          email: email,
        });
        navigate('/dashboard');
      } else {
        setError('Invalid email or password (min 6 chars)');
        setIsLoading(false);
      }
    }, 1000);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="glass w-full max-w-md p-8 rounded-2xl relative overflow-hidden">
        {/* Decorative background blob */}
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#7C3AED] to-[#6D28D9]" />

        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h2>
          <p className="text-gray-500">Sign in to continue to EventFlow</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-500 text-sm rounded-lg border border-red-100 flex items-center justify-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
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
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <a href="#" className="text-xs text-[#6D28D9] font-semibold hover:underline">Forgot password?</a>
            </div>
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
            className="w-full bg-[#6D28D9] hover:bg-[#5b21b6] text-white font-bold py-3 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed shadow-lg shadow-purple-200"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Sign In <ArrowRight className="w-5 h-5" /></>}
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-gray-500">
          Don't have an account?{' '}
          <Link to="/signup" className="text-[#6D28D9] font-bold hover:underline">
            Create account
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;