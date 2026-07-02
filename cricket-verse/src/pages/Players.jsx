import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { mockPlayers } from '../data/mockData';
import { User, Search, Filter } from 'lucide-react';

export default function Players() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('All');

  const filteredPlayers = mockPlayers.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          player.team.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = filterRole === 'All' || player.role === filterRole;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <h2 className="text-3xl font-bold flex items-center gap-3">
            <User className="w-8 h-8 text-cricket-blue" />
            Player Profiles
          </h2>
          
          <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                type="text" 
                placeholder="Search players, teams..." 
                className="w-full sm:w-64 pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full focus:outline-none focus:border-cricket-blue text-white"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="relative flex-shrink-0">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <select 
                className="w-full sm:w-auto pl-10 pr-8 py-2 bg-[#1a2235] border border-white/10 rounded-full focus:outline-none focus:border-cricket-blue text-white appearance-none cursor-pointer"
                value={filterRole}
                onChange={(e) => setFilterRole(e.target.value)}
              >
                <option value="All">All Roles</option>
                <option value="Batsman">Batsman</option>
                <option value="Bowler">Bowler</option>
                <option value="All-rounder">All-rounder</option>
              </select>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredPlayers.map((player, index) => (
            <motion.div
              key={player.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5 }}
              className="glass-card rounded-2xl overflow-hidden group"
            >
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={player.image} 
                  alt={player.name} 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
                <div className="absolute bottom-4 left-4">
                  <h3 className="text-xl font-bold text-white">{player.name}</h3>
                  <p className="text-cricket-gold text-sm font-semibold">{player.team}</p>
                </div>
                <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm px-2 py-1 rounded text-xs font-bold border border-white/10">
                  {player.role}
                </div>
              </div>
              
              <div className="p-4 bg-white/5">
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-xs text-gray-400 uppercase tracking-wider">Matches</div>
                    <div className="font-bold text-lg">{player.matches}</div>
                  </div>
                  {player.role === 'Batsman' || player.role === 'All-rounder' ? (
                    <div>
                      <div className="text-xs text-gray-400 uppercase tracking-wider">Average</div>
                      <div className="font-bold text-lg">{player.average}</div>
                    </div>
                  ) : null}
                  {player.role === 'Bowler' || player.role === 'All-rounder' ? (
                    <div>
                      <div className="text-xs text-gray-400 uppercase tracking-wider">Wickets</div>
                      <div className="font-bold text-lg">{player.wickets}</div>
                    </div>
                  ) : null}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        
        {filteredPlayers.length === 0 && (
          <div className="text-center py-12 text-gray-400">
            No players found matching your criteria.
          </div>
        )}
      </motion.div>
    </div>
  );
}
