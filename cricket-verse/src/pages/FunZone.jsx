import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gamepad2, Lightbulb, Dices, Gift } from 'lucide-react';
import { mockTrivia } from '../data/mockData';

export default function FunZone() {
  const [triviaIndex, setTriviaIndex] = useState(0);
  const [spinning, setSpinning] = useState(false);
  const [prize, setPrize] = useState(null);

  const getNewTrivia = () => {
    setTriviaIndex((prev) => (prev + 1) % mockTrivia.length);
  };

  const spinWheel = () => {
    if (spinning) return;
    setSpinning(true);
    setPrize(null);
    
    // Simulate spin
    setTimeout(() => {
      const prizes = ['Free Ticket Entry', 'Signed Bat', 'VIP Pass', 'Better Luck Next Time', 'Team Jersey'];
      setPrize(prizes[Math.floor(Math.random() * prizes.length)]);
      setSpinning(false);
    }, 2000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <Gamepad2 className="w-8 h-8 text-cricket-blue" />
          Fan Fun Zone
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Trivia Generator */}
          <motion.div 
            whileHover={{ y: -5 }}
            className="glass-card rounded-3xl p-8 bg-gradient-to-br from-white/5 to-cricket-blue/10 border-cricket-blue/30"
          >
            <div className="flex items-center gap-3 mb-6">
              <Lightbulb className="w-6 h-6 text-yellow-400" />
              <h3 className="text-xl font-bold">Random Trivia Generator</h3>
            </div>
            
            <AnimatePresence mode="wait">
              <motion.div 
                key={triviaIndex}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="bg-black/20 p-6 rounded-xl min-h-[120px] flex items-center mb-6 italic text-gray-200"
              >
                "{mockTrivia[triviaIndex]}"
              </motion.div>
            </AnimatePresence>
            
            <button 
              onClick={getNewTrivia}
              className="w-full py-3 bg-white/10 hover:bg-white/20 rounded-full font-semibold transition-colors flex items-center justify-center gap-2 border border-white/20"
            >
              <Dices className="w-5 h-5" /> Give me another fact
            </button>
          </motion.div>

          {/* Spin the Wheel */}
          <motion.div 
            whileHover={{ y: -5 }}
            className="glass-card rounded-3xl p-8 bg-gradient-to-br from-white/5 to-cricket-gold/10 border-cricket-gold/30 flex flex-col items-center justify-center text-center"
          >
            <div className="flex items-center gap-3 mb-4">
              <Gift className="w-6 h-6 text-cricket-gold" />
              <h3 className="text-xl font-bold">Spin to Win!</h3>
            </div>
            <p className="text-sm text-gray-400 mb-8">Try your luck for exclusive CricketVerse merchandise and tickets.</p>
            
            <div className="relative w-48 h-48 mb-8">
              <motion.div 
                animate={{ rotate: spinning ? 1440 : 0 }}
                transition={{ duration: 2, ease: "circOut" }}
                className="w-full h-full rounded-full border-4 border-cricket-gold border-dashed bg-gradient-to-tr from-cricket-blue to-purple-600 flex items-center justify-center shadow-[0_0_30px_rgba(251,191,36,0.3)]"
              >
                <span className="font-bold text-2xl tracking-widest text-white/50">SPIN</span>
              </motion.div>
              {/* Pointer */}
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[15px] border-l-transparent border-r-[15px] border-r-transparent border-t-[30px] border-t-white drop-shadow-lg z-10" />
            </div>

            <AnimatePresence>
              {prize && !spinning && (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="mb-6 p-4 bg-green-500/20 border border-green-500 rounded-xl text-green-400 font-bold w-full"
                >
                  You won: {prize}
                </motion.div>
              )}
            </AnimatePresence>

            <button 
              onClick={spinWheel}
              disabled={spinning}
              className={`w-full py-3 bg-gradient-to-r from-cricket-gold to-yellow-600 hover:from-yellow-500 hover:to-yellow-700 text-black rounded-full font-bold text-lg transition-all shadow-lg ${spinning ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {spinning ? 'Spinning...' : 'Spin the Wheel'}
            </button>
          </motion.div>
          
        </div>
      </motion.div>
    </div>
  );
}
