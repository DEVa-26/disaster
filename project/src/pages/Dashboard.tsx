import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div 
      className="min-h-screen relative flex items-center justify-center"
      style={{
        backgroundImage: 'url("https://images.unsplash.com/photo-1547683905-f686c993c794?auto=format&fit=crop&w=2000&q=80")',
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 to-black/40" />
      
      <div className="relative text-center text-white px-4 max-w-5xl mx-auto">
        <div className="flex items-center justify-center mb-6">
          <AlertTriangle className="h-16 w-16 text-red-500 mr-4" />
          <h1 className="text-6xl md:text-7xl font-bold">
            Disaster Management Pro
          </h1>
        </div>
        
        <p className="text-xl md:text-2xl mb-12 text-gray-200">
          Your comprehensive solution for disaster management and response coordination. 
          We help organizations prepare, respond, and recover from emergencies.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link to="/disaster-identifier">
            <Button variant="emergency" size="lg" className="text-lg px-8 py-6">
              Identify Disaster
            </Button>
          </Link>
          <Link to="/login">
            <Button variant="outline" size="lg" className="text-lg px-8 py-6 bg-white/10 hover:bg-white/20 border-white">
              Emergency Login
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;