import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { mockMatches } from '../data/mockData';
import { Activity, Clock, CheckCircle } from 'lucide-react';

export default function LiveScores() {
  const [matches, setMatches] = useState(mockMatches);

  // Simulate live score updates
  useEffect(() => {
    const interval = setInterval(() => {
      setMatches(current => 
        current.map(match => {
          if (match.status === 'live') {
            // Randomly update overs and scores to simulate live action
            const newRuns = Math.floor(Math.random() * 6);
            return {
              ...match,
              team1: {
                ...match.team1,
                score: `${parseInt(match.team1.score.split('/')[0]) + newRuns}/${match.team1.score.split('/')[1]}`
              }
            };
          }
          return match;
        })
      );
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch(status) {
      case 'live': return <Activity className="w-4 h-4 text-red-500 animate-pulse" />;
      case 'upcoming': return <Clock className="w-4 h-4 text-cricket-gold" />;
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />;
      default: return null;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <Activity className="w-8 h-8 text-cricket-blue" />
          Live Scores & Updates
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match) => (
            <motion.div 
              key={match.id}
              whileHover={{ y: -5 }}
              className="glass-card rounded-2xl p-6 relative overflow-hidden"
            >
              <div className="flex justify-between items-center mb-4">
                <span className="text-sm text-gray-400 font-medium tracking-wider uppercase">
                  {match.type}
                </span>
                <span className="flex items-center gap-2 text-sm font-semibold capitalize bg-white/10 px-3 py-1 rounded-full">
                  {getStatusIcon(match.status)}
                  {match.status}
                </span>
              </div>

              <div className="space-y-4">
                {/* Team 1 */}
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{match.team1.logo}</span>
                    <span className="font-bold text-lg">{match.team1.code}</span>
                  </div>
                  <div className="text-right">
                    {match.team1.score && (
                      <div className="font-bold text-xl">{match.team1.score}</div>
                    )}
                    {match.team1.overs && (
                      <div className="text-sm text-gray-400">({match.team1.overs} ov)</div>
                    )}
                  </div>
                </div>

                {/* Team 2 */}
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{match.team2.logo}</span>
                    <span className="font-bold text-lg">{match.team2.code}</span>
                  </div>
                  <div className="text-right">
                    {match.team2.score ? (
                      <div className="font-bold text-xl">{match.team2.score}</div>
                    ) : (
                      <div className="font-bold text-lg text-gray-500">Yet to bat</div>
                    )}
                    {match.team2.overs && (
                      <div className="text-sm text-gray-400">({match.team2.overs} ov)</div>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-white/10 text-sm text-cricket-gold font-medium">
                {match.summary || match.time}
              </div>
              
              {/* Highlight bar for live matches */}
              {match.status === 'live' && (
                <div className="absolute bottom-0 left-0 h-1 bg-red-500 animate-pulse w-full" />
              )}
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
