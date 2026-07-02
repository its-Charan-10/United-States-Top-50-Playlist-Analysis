import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, PlayCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Image Overlay */}
      <div 
        className="absolute inset-0 z-0 opacity-20"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-cricket-dark/80 via-cricket-dark to-cricket-dark z-0" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-16 text-center lg:text-left">
        <div className="lg:w-2/3">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
              Live. Play. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cricket-gold to-yellow-200">
                Celebrate Cricket.
              </span>
            </h1>
            <p className="mt-4 text-xl text-gray-300 mb-10 max-w-2xl mx-auto lg:mx-0">
              Your ultimate destination for live scores, in-depth stats, interactive games, and everything cricket. Step into the CricketVerse.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link to="/scores">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full sm:w-auto px-8 py-4 bg-cricket-blue hover:bg-blue-600 text-white rounded-full font-semibold text-lg flex items-center justify-center gap-2 transition-colors shadow-[0_0_20px_rgba(59,130,246,0.5)]"
                >
                  <PlayCircle className="w-5 h-5" />
                  Live Action
                </motion.button>
              </Link>
              <Link to="/teams">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full sm:w-auto px-8 py-4 bg-white/10 hover:bg-white/20 text-white rounded-full font-semibold text-lg flex items-center justify-center gap-2 backdrop-blur-sm transition-colors border border-white/10"
                >
                  Explore Teams
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Decorative elements - Animated Bat & Ball */}
        <div className="hidden lg:block absolute right-10 top-1/2 -translate-y-1/2">
          <motion.div
            initial={{ opacity: 0, scale: 0.5, rotate: -45 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            transition={{ duration: 1, delay: 0.5 }}
            className="relative"
          >
            <div className="w-64 h-64 bg-gradient-to-br from-cricket-gold/20 to-cricket-blue/20 rounded-full blur-3xl absolute -inset-4" />
            <img 
              src="https://images.unsplash.com/photo-1531415074968-036ba1b575da?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60" 
              alt="Cricket Action" 
              className="w-96 h-96 object-cover rounded-3xl shadow-2xl border-4 border-white/10 rotate-12"
            />
          </motion.div>
        </div>
      </div>
    </div>
  );
}
