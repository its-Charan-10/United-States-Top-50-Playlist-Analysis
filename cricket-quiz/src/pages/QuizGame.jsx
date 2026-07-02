import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { quizData } from '../data/questions';
import { Timer, X, CheckCircle2, XCircle, ChevronRight, Zap } from 'lucide-react';

const levelAccentColors = {
  easy: { bg: 'bg-emerald-500', text: 'text-emerald-400', ring: 'ring-emerald-500/30', bar: 'bg-emerald-500' },
  medium: { bg: 'bg-amber-500', text: 'text-amber-400', ring: 'ring-amber-500/30', bar: 'bg-amber-500' },
  hard: { bg: 'bg-rose-500', text: 'text-rose-400', ring: 'ring-rose-500/30', bar: 'bg-rose-500' },
};

export default function QuizGame({ level, onFinish, onQuit }) {
  const data = quizData[level];
  const questions = data.questions;
  const colors = levelAccentColors[level];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  const [timeLeft, setTimeLeft] = useState(data.timePerQuestion);
  const [answers, setAnswers] = useState([]);

  const current = questions[currentIndex];
  const progress = ((currentIndex) / questions.length) * 100;

  // Timer countdown
  useEffect(() => {
    if (selected !== null) return;
    if (timeLeft <= 0) {
      handleTimeout();
      return;
    }
    const timer = setTimeout(() => setTimeLeft(t => t - 1), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft, selected]);

  const handleTimeout = useCallback(() => {
    setAnswers(prev => [...prev, { question: currentIndex, selected: -1, correct: current.correct, timedOut: true }]);
    setStreak(0);
    setTimeout(() => advance(), 1200);
  }, [currentIndex, current]);

  const handleSelect = (optionIndex) => {
    if (selected !== null) return;
    setSelected(optionIndex);

    const isCorrect = optionIndex === current.correct;
    if (isCorrect) {
      const timeBonus = Math.floor(timeLeft / data.timePerQuestion * data.points * 0.5);
      setScore(prev => prev + data.points + timeBonus);
      setStreak(prev => {
        const newStreak = prev + 1;
        if (newStreak > bestStreak) setBestStreak(newStreak);
        return newStreak;
      });
    } else {
      setStreak(0);
    }

    setAnswers(prev => [...prev, { question: currentIndex, selected: optionIndex, correct: current.correct, timedOut: false }]);
    setTimeout(() => advance(), 1200);
  };

  const advance = () => {
    if (currentIndex + 1 >= questions.length) {
      const correctCount = answers.length > 0
        ? answers.filter(a => a.selected === a.correct).length + (selected === current.correct ? 1 : 0)
        : (selected === current.correct ? 1 : 0);
      
      // Calculate final correct count from all answers
      const allAnswers = [...answers, { question: currentIndex, selected: selected ?? -1, correct: current.correct, timedOut: selected === null }];
      const finalCorrect = allAnswers.filter(a => a.selected === a.correct).length;

      onFinish({
        level,
        score: score + (selected === current.correct ? data.points : 0),
        totalQuestions: questions.length,
        correctAnswers: finalCorrect,
        percentage: Math.round((finalCorrect / questions.length) * 100),
        bestStreak: Math.max(bestStreak, selected === current.correct ? streak + 1 : streak),
        answers: allAnswers,
      });
      return;
    }

    setCurrentIndex(prev => prev + 1);
    setSelected(null);
    setTimeLeft(data.timePerQuestion);
  };

  const timerColor = timeLeft <= 5 ? 'text-rose-400' : timeLeft <= 10 ? 'text-amber-400' : 'text-white/60';
  const timerBarWidth = (timeLeft / data.timePerQuestion) * 100;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="pt-24 pb-16 px-4 sm:px-6"
    >
      <div className="max-w-2xl mx-auto">
        {/* Top bar: Progress + Quit */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <span className="text-lg">{data.emoji}</span>
            <span className="text-sm font-semibold text-white/50">{data.label} Level</span>
          </div>
          <button
            onClick={onQuit}
            className="flex items-center gap-1.5 text-sm text-white/30 hover:text-white/60 transition-colors"
          >
            <X className="w-4 h-4" />
            Quit
          </button>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-1.5 bg-white/[0.06] rounded-full mb-8 overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${colors.bar}`}
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>

        {/* Stats Row */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="glass rounded-xl px-3 py-2 flex items-center gap-2">
              <Zap className={`w-4 h-4 ${colors.text}`} />
              <span className="text-sm font-bold">{score}</span>
              <span className="text-xs text-white/30">pts</span>
            </div>
            {streak >= 2 && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="glass rounded-xl px-3 py-2 flex items-center gap-1.5 text-sm"
              >
                🔥 <span className="font-bold">{streak}</span>
                <span className="text-xs text-white/30">streak</span>
              </motion.div>
            )}
          </div>
          <div className={`flex items-center gap-2 ${timerColor} font-mono text-sm font-bold`}>
            <Timer className="w-4 h-4" />
            {timeLeft}s
          </div>
        </div>

        {/* Timer Bar */}
        <div className="w-full h-0.5 bg-white/[0.04] rounded-full mb-8 overflow-hidden">
          <motion.div
            className={`h-full rounded-full transition-colors duration-300 ${timeLeft <= 5 ? 'bg-rose-500' : timeLeft <= 10 ? 'bg-amber-500' : colors.bar}`}
            animate={{ width: `${timerBarWidth}%` }}
            transition={{ duration: 0.8 }}
          />
        </div>

        {/* Question */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.3 }}
          >
            <div className="mb-3 text-xs text-white/30 font-medium tracking-wider uppercase">
              Question {currentIndex + 1} of {questions.length}
            </div>
            <h2 className="text-xl sm:text-2xl font-bold mb-8 leading-relaxed">
              {current.question}
            </h2>

            {/* Options */}
            <div className="space-y-3">
              {current.options.map((option, idx) => {
                let classes = 'w-full text-left p-4 sm:p-5 rounded-xl border transition-all duration-200 flex items-center justify-between group ';

                if (selected === null && timeLeft > 0) {
                  classes += 'bg-white/[0.03] border-white/[0.08] hover:bg-white/[0.07] hover:border-white/[0.15] cursor-pointer';
                } else if (idx === current.correct) {
                  classes += 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300';
                } else if (idx === selected && idx !== current.correct) {
                  classes += 'bg-rose-500/15 border-rose-500/40 text-rose-300';
                } else {
                  classes += 'bg-white/[0.02] border-white/[0.04] opacity-40';
                }

                return (
                  <motion.button
                    key={idx}
                    onClick={() => handleSelect(idx)}
                    disabled={selected !== null || timeLeft <= 0}
                    whileHover={selected === null && timeLeft > 0 ? { scale: 1.01 } : {}}
                    whileTap={selected === null && timeLeft > 0 ? { scale: 0.99 } : {}}
                    className={classes}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-7 h-7 rounded-lg bg-white/[0.06] border border-white/[0.08] flex items-center justify-center text-xs font-bold text-white/40 shrink-0">
                        {String.fromCharCode(65 + idx)}
                      </span>
                      <span className="font-medium text-sm sm:text-base">{option}</span>
                    </div>
                    {selected !== null && idx === current.correct && (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                    )}
                    {selected === idx && idx !== current.correct && (
                      <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                    )}
                  </motion.button>
                );
              })}
            </div>

            {/* Timed out message */}
            {timeLeft <= 0 && selected === null && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 text-center text-rose-400 text-sm font-medium"
              >
                ⏱️ Time's up! The correct answer was highlighted.
              </motion.div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
