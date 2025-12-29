import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Calendar, Users, Globe } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 left-0 w-full h-full bg-white z-0" />
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-purple-200 rounded-full blur-[100px] opacity-40" />
        <div className="absolute bottom-[-20%] left-[-10%] w-[500px] h-[500px] bg-blue-200 rounded-full blur-[100px] opacity-40" />

        <div className="container mx-auto px-4 pt-20 pb-32 relative z-10">
          <div className="text-center max-w-4xl mx-auto">
            <span className="inline-block py-1 px-3 rounded-full bg-purple-50 border border-purple-100 text-[#6D28D9] text-sm font-bold mb-6 tracking-wide">
              🚀 The #1 Platform for Event Discovery
            </span>
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 leading-tight mb-8">
              Find your next <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#6D28D9] to-blue-600">
                unforgettable experience
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              Join thousands of people discovering conferences, workshops, concerts, and meetups. 
              Your personalized event journey starts here.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link 
                to="/dashboard" 
                className="w-full sm:w-auto px-8 py-4 bg-[#6D28D9] text-white rounded-xl font-bold text-lg hover:bg-[#5b21b6] transition-all shadow-lg hover:shadow-purple-200 flex items-center justify-center gap-2"
              >
                Explore Events <ArrowRight className="w-5 h-5" />
              </Link>
              <Link 
                to="/signup" 
                className="w-full sm:w-auto px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-xl font-bold text-lg hover:bg-gray-50 transition-all"
              >
                Create Account
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<Calendar className="w-8 h-8 text-[#6D28D9]" />}
              title="Smart Aggregation"
              description="We pull events from multiple platforms so you don't have to check ten different websites."
            />
            <FeatureCard 
              icon={<Users className="w-8 h-8 text-blue-600" />}
              title="Social Connection"
              description="See where your friends are going and meet like-minded people at events you love."
            />
            <FeatureCard 
              icon={<Globe className="w-8 h-8 text-indigo-600" />}
              title="Global Reach"
              description="From local meetups in your city to major global conferences, we cover it all."
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper component for features
const FeatureCard: React.FC<{ icon: React.ReactNode; title: string; description: string }> = ({ icon, title, description }) => (
  <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
    <div className="bg-gray-50 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
    <p className="text-gray-500 leading-relaxed">{description}</p>
  </div>
);

export default Home;