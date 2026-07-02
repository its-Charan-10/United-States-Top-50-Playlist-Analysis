import React from 'react';
import { motion } from 'framer-motion';
import { quizData } from '../data/questions';
import { Trophy, Star, Flame, RotateCcw, Home, CheckCircle2, XCircle, Clock } from 'lucide-react';

const gradeEmoji = (pct) => {
  if (pct === 100) return { emoji: '🏆', label: 'Perfect Score!', color: 'text-amber-400' };
  if (pct >= 80) return { emoji: '🌟', label: 'Excellent!', color: 'text-emerald-400' };
  if (pct >= 60) return { emoji: '👏', label: 'Well Done!', color: 'text-blue-400' };
  if (pct >= 40) return { emoji: '📚', label: 'Keep Learning!', color: 'text-amber-400' };
  return { emoji: '💪', label: 'Try Again!', color: 'text-rose-400' };
};

export default function Results({ result, onRetry, onHome }) {
  const { level, score, totalQuestions, correctAnswers, percentage, bestStreak, answers } = result;
  const data = quizData[level];
  const grade = gradeEmoji(percentage);
  const passed = percentage >= 60;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="pt-24 pb-16 px-4 sm:px-6"
    >
      <div className="max-w-2xl mx-auto">
        {/* Result Hero */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            className="text-7xl mb-4"
          >
            {grade.emoji}
          </motion.div>
          <h2 className={`text-3xl sm:text-4xl font-extrabold mb-2 ${grade.color}`}>
            {grade.label}
          </h2>
          <p className="text-white/40 text-sm">
            {data.label} Level Complete
          </p>
        </motion.div>

        {/* Score Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass rounded-2xl p-6 mb-6"
        >
          {/* Big Score */}
          <div className="text-center mb-6 pb-6 border-b border-white/[0.06]">
            <div className="text-5xl font-extrabold text-gradient-gold mb-1">{score}</div>
            <div className="text-sm text-white/30">Total Points</div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="flex items-center justify-center gap-1.5 mb-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span className="text-xl font-bold">{correctAnswers}</span>
              </div>
              <div className="text-xs text-white/30">Correct</div>
            </div>
            <div>
              <div className="flex items-center justify-center gap-1.5 mb-1">
                <Star className="w-4 h-4 text-amber-400" />
                <span className="text-xl font-bold">{percentage}%</span>
              </div>
              <div className="text-xs text-white/30">Accuracy</div>
            </div>
            <div>
              <div className="flex items-center justify-center gap-1.5 mb-1">
                <Flame className="w-4 h-4 text-rose-400" />
                <span className="text-xl font-bold">{bestStreak}</span>
              </div>
              <div className="text-xs text-white/30">Best Streak</div>
            </div>
          </div>
        </motion.div>

        {/* Level Unlock */}
        {passed && level !== 'hard' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="glass rounded-2xl p-4 mb-6 border-emerald-500/20 bg-emerald-500/5 text-center"
          >
            <div className="text-emerald-400 text-sm font-semibold flex items-center justify-center gap-2">
              <Trophy className="w-4 h-4" />
              🎉 Next level unlocked!
            </div>
          </motion.div>
        )}

        {/* Answer Review */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="glass rounded-2xl p-6 mb-8"
        >
          <h3 className="text-sm font-semibold text-white/50 mb-4 uppercase tracking-wider">Answer Review</h3>
          <div className="space-y-3">
            {answers.map((answer, idx) => {
              const q = data.questions[answer.question];
              const isCorrect = answer.selected === answer.correct;
              return (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border text-sm ${
                    answer.timedOut
                      ? 'bg-white/[0.02] border-white/[0.06]'
                      : isCorrect
                      ? 'bg-emerald-500/5 border-emerald-500/15'
                      : 'bg-rose-500/5 border-rose-500/15'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <div className="shrink-0 mt-0.5">
                      {answer.timedOut ? (
                        <Clock className="w-4 h-4 text-white/30" />
                      ) : isCorrect ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-white/70 mb-1 leading-snug">{q.question}</div>
                      {answer.timedOut ? (
                        <div className="text-white/30 text-xs">Time expired — Answer: <span className="text-emerald-400">{q.options[answer.correct]}</span></div>
                      ) : !isCorrect ? (
                        <div className="text-xs">
                          <span className="text-rose-400 line-through">{q.options[answer.selected]}</span>
                          <span className="text-white/30 mx-1">→</span>
                          <span className="text-emerald-400">{q.options[answer.correct]}</span>
                        </div>
                      ) : (
                        <div className="text-emerald-400 text-xs">{q.options[answer.correct]}</div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <button
            onClick={onRetry}
            className="flex-1 flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-white/[0.06] hover:bg-white/[0.1] border border-white/[0.08] text-sm font-semibold transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Try Again
          </button>
          <button
            onClick={onHome}
            className="flex-1 flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-cricket-blue hover:bg-blue-500 text-sm font-semibold transition-colors shadow-lg"
          >
            <Home className="w-4 h-4" />
            Back to Levels
          </button>
        </motion.div>
      </div>
    </motion.div>
  );
}
