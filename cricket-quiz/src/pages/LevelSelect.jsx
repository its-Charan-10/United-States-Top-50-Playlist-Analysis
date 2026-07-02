import React from 'react';
import { motion } from 'framer-motion';
import { quizData } from '../data/questions';
import { Brain, Zap, Flame, Lock, CheckCircle2, ArrowRight, ChevronRight } from 'lucide-react';

const levelIcons = { easy: Brain, medium: Zap, hard: Flame };
const levelOrder = ['easy', 'medium', 'hard'];

const levelGradients = {
  easy: 'from-emerald-500/20 to-emerald-900/10',
  medium: 'from-amber-500/20 to-amber-900/10',
  hard: 'from-rose-500/20 to-rose-900/10',
};

const levelBorders = {
  easy: 'border-emerald-500/20 hover:border-emerald-500/40',
  medium: 'border-amber-500/20 hover:border-amber-500/40',
  hard: 'border-rose-500/20 hover:border-rose-500/40',
};

const levelGlows = {
  easy: 'glow-emerald',
  medium: 'glow-gold',
  hard: 'glow-rose',
};

const levelTextColors = {
  easy: 'text-emerald-400',
  medium: 'text-amber-400',
  hard: 'text-rose-400',
};

const levelBtnBg = {
  easy: 'bg-emerald-500 hover:bg-emerald-400',
  medium: 'bg-amber-500 hover:bg-amber-400',
  hard: 'bg-rose-500 hover:bg-rose-400',
};

export default function LevelSelect({ onSelectLevel, completedLevels }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="pt-28 pb-16 px-4 sm:px-6"
    >
      <div className="max-w-4xl mx-auto">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 bg-white/[0.04] border border-white/[0.08] rounded-full px-4 py-1.5 text-sm text-white/50 mb-6">
            <span className="text-lg">🏏</span>
            <span>Test Your Cricket Knowledge</span>
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-5 leading-tight">
            How Well Do You<br />
            <span className="text-gradient-gold">Know Cricket?</span>
          </h1>
          <p className="text-lg text-white/40 max-w-xl mx-auto leading-relaxed">
            Challenge yourself across three difficulty levels. From beginner basics
            to expert trivia — prove you're the ultimate cricket fan.
          </p>
        </motion.div>

        {/* Level Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {levelOrder.map((key, index) => {
            const level = quizData[key];
            const Icon = levelIcons[key];
            const isCompleted = completedLevels.includes(key);
            const isLocked = index > 0 && !completedLevels.includes(levelOrder[index - 1]);

            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 * index, duration: 0.5 }}
              >
                <motion.button
                  whileHover={!isLocked ? { y: -6, scale: 1.01 } : {}}
                  whileTap={!isLocked ? { scale: 0.98 } : {}}
                  onClick={() => !isLocked && onSelectLevel(key)}
                  disabled={isLocked}
                  className={`
                    w-full text-left p-6 rounded-2xl border transition-all duration-300 relative overflow-hidden
                    bg-gradient-to-br ${levelGradients[key]} ${levelBorders[key]}
                    ${isLocked ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}
                    ${!isLocked ? levelGlows[key] : ''}
                  `}
                >
                  {/* Completed badge */}
                  {isCompleted && (
                    <div className="absolute top-4 right-4">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    </div>
                  )}

                  {/* Locked badge */}
                  {isLocked && (
                    <div className="absolute top-4 right-4">
                      <Lock className="w-5 h-5 text-white/30" />
                    </div>
                  )}

                  {/* Icon */}
                  <div className={`w-12 h-12 rounded-xl bg-white/[0.06] border border-white/[0.08] flex items-center justify-center mb-5`}>
                    <Icon className={`w-6 h-6 ${levelTextColors[key]}`} />
                  </div>

                  {/* Title */}
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xl">{level.emoji}</span>
                    <h3 className="text-xl font-bold">{level.label}</h3>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-white/40 mb-5 leading-relaxed">
                    {level.description}
                  </p>

                  {/* Stats */}
                  <div className="flex items-center gap-4 text-xs text-white/30 mb-5">
                    <span>{level.questions.length} questions</span>
                    <span>•</span>
                    <span>{level.points} pts each</span>
                    <span>•</span>
                    <span>{level.timePerQuestion}s timer</span>
                  </div>

                  {/* Button */}
                  {!isLocked && (
                    <div className={`flex items-center justify-center gap-2 w-full py-2.5 rounded-xl text-sm font-semibold text-white ${levelBtnBg[key]} transition-colors`}>
                      {isCompleted ? 'Play Again' : 'Start Quiz'}
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  )}
                  {isLocked && (
                    <div className="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl text-sm font-medium text-white/20 bg-white/[0.04] border border-white/[0.06]">
                      <Lock className="w-3.5 h-3.5" />
                      Complete {quizData[levelOrder[index - 1]].label} First
                    </div>
                  )}
                </motion.button>
              </motion.div>
            );
          })}
        </div>

        {/* Bottom info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="text-center mt-12 text-sm text-white/25"
        >
          Score 60% or higher to unlock the next level
        </motion.div>
      </div>
    </motion.div>
  );
}
