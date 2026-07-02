import React from 'react';
import { motion } from 'framer-motion';
import { mockTeams } from '../data/mockData';
import { Users, Shield, Star } from 'lucide-react';

export default function Teams() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <Users className="w-8 h-8 text-cricket-blue" />
          International Teams
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockTeams.map((team, index) => (
            <motion.div
              key={team.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="glass-card rounded-2xl p-6 group cursor-pointer"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="text-4xl shadow-sm">{team.flag}</div>
                <div className="flex items-center gap-1 bg-cricket-gold/20 text-cricket-gold px-3 py-1 rounded-full text-sm font-bold">
                  <Star className="w-4 h-4 fill-current" />
                  Rank {team.ranking}
                </div>
              </div>
              
              <h3 className="text-2xl font-bold mb-2 group-hover:text-cricket-blue transition-colors">
                {team.name}
              </h3>
              
              <div className="flex items-center gap-2 text-gray-300">
                <Shield className="w-4 h-4" />
                <span className="text-sm">Captain: <span className="font-semibold text-white">{team.captain}</span></span>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
