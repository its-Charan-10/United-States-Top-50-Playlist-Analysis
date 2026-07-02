import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, Video, ArrowRight } from 'lucide-react';
import { mockMatches } from '../data/mockData';

export default function MatchCenter() {
  const upcomingMatches = mockMatches.filter(m => m.status === 'upcoming');
  const recentMatches = mockMatches.filter(m => m.status === 'completed');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <Calendar className="w-8 h-8 text-cricket-blue" />
          Match Center
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <section>
              <h3 className="text-xl font-bold mb-4 text-cricket-gold border-b border-white/10 pb-2">Recent Results</h3>
              <div className="space-y-4">
                {recentMatches.map((match, idx) => (
                  <motion.div 
                    key={match.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass-card rounded-xl p-4 flex flex-col sm:flex-row justify-between items-center gap-4 hover:bg-white/10 transition-colors cursor-pointer"
                  >
                    <div className="flex-1 w-full sm:w-auto">
                      <div className="text-xs text-gray-400 mb-2">{match.type}</div>
                      <div className="flex justify-between items-center bg-black/20 p-2 rounded mb-1">
                        <span className="flex items-center gap-2"><span className="text-xl">{match.team1.logo}</span> {match.team1.name}</span>
                        <span className="font-bold">{match.team1.score}</span>
                      </div>
                      <div className="flex justify-between items-center bg-black/20 p-2 rounded">
                        <span className="flex items-center gap-2"><span className="text-xl">{match.team2.logo}</span> {match.team2.name}</span>
                        <span className="font-bold">{match.team2.score}</span>
                      </div>
                    </div>
                    <div className="flex flex-col items-center sm:items-end min-w-[120px]">
                      <div className="text-sm font-semibold text-cricket-blue mb-2 text-center sm:text-right">{match.summary}</div>
                      <button className="flex items-center gap-1 text-xs bg-white/5 hover:bg-white/10 px-3 py-1.5 rounded-full transition-colors border border-white/10">
                        <Video className="w-3 h-3" /> Highlights
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </section>
          </div>

          <div className="space-y-8">
            <section>
              <h3 className="text-xl font-bold mb-4 text-cricket-gold border-b border-white/10 pb-2">Upcoming Fixtures</h3>
              <div className="space-y-4">
                {upcomingMatches.map((match, idx) => (
                  <motion.div 
                    key={match.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass-card rounded-xl p-4"
                  >
                    <div className="text-xs text-gray-400 mb-3 text-center">{match.type}</div>
                    <div className="flex justify-center items-center gap-4 mb-3">
                      <div className="flex flex-col items-center">
                        <span className="text-3xl mb-1">{match.team1.logo}</span>
                        <span className="font-bold text-sm">{match.team1.code}</span>
                      </div>
                      <div className="text-gray-500 font-bold italic">VS</div>
                      <div className="flex flex-col items-center">
                        <span className="text-3xl mb-1">{match.team2.logo}</span>
                        <span className="font-bold text-sm">{match.team2.code}</span>
                      </div>
                    </div>
                    <div className="text-center text-sm font-semibold bg-cricket-blue/20 text-blue-200 py-1.5 rounded-md mt-2">
                      {match.time}
                    </div>
                  </motion.div>
                ))}
              </div>
              <button className="w-full mt-4 flex items-center justify-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
                View Full Schedule <ArrowRight className="w-4 h-4" />
              </button>
            </section>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
