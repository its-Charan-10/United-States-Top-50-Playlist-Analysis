import React from 'react';
import { motion } from 'framer-motion';
import { Trophy } from 'lucide-react';

export default function Header({ onLogoClick }) {
  return (
    <header className="glass-strong fixed top-0 w-full z-50 border-b border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <motion.button
          onClick={onLogoClick}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2.5 cursor-pointer"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cricket-gold to-amber-600 flex items-center justify-center shadow-lg">
            <Trophy className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">
            Cricket<span className="text-gradient-gold">Quiz</span>
          </span>
        </motion.button>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-1.5 text-xs text-white/40 bg-white/[0.04] px-3 py-1.5 rounded-full border border-white/[0.06]">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>Easy → Medium → Hard</span>
          </div>
        </div>
      </div>
    </header>
  );
}
