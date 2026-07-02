import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, CheckCircle2, XCircle, Trophy } from 'lucide-react';

const quizQuestions = [
  {
    question: "Who holds the record for the highest individual score in ODI cricket?",
    options: ["Sachin Tendulkar", "Martin Guptill", "Rohit Sharma", "Virender Sehwag"],
    correctAnswer: 2
  },
  {
    question: "Which team won the first ever Cricket World Cup in 1975?",
    options: ["Australia", "West Indies", "England", "India"],
    correctAnswer: 1
  },
  {
    question: "What is the length of a standard cricket pitch?",
    options: ["20 yards", "22 yards", "24 yards", "26 yards"],
    correctAnswer: 1
  }
];

export default function Quiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);

  const handleAnswerClick = (index) => {
    if (selectedOption !== null) return;
    
    setSelectedOption(index);
    
    if (index === quizQuestions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }

    setTimeout(() => {
      const nextQuestion = currentQuestion + 1;
      if (nextQuestion < quizQuestions.length) {
        setCurrentQuestion(nextQuestion);
        setSelectedOption(null);
      } else {
        setShowScore(true);
      }
    }, 1500);
  };

  const restartQuiz = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowScore(false);
    setSelectedOption(null);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card rounded-3xl p-8 shadow-[0_0_40px_rgba(59,130,246,0.1)]"
      >
        <div className="flex items-center justify-center gap-3 mb-8 border-b border-white/10 pb-6">
          <Brain className="w-10 h-10 text-cricket-blue" />
          <h2 className="text-3xl font-bold">Cricket IQ Test</h2>
        </div>

        <AnimatePresence mode="wait">
          {showScore ? (
            <motion.div 
              key="score"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="text-center py-8"
            >
              <Trophy className="w-24 h-24 mx-auto text-cricket-gold mb-6" />
              <h3 className="text-3xl font-bold mb-4">Quiz Completed!</h3>
              <p className="text-xl text-gray-300 mb-8">
                You scored <span className="text-cricket-gold font-bold text-3xl">{score}</span> out of {quizQuestions.length}
              </p>
              <button 
                onClick={restartQuiz}
                className="px-8 py-3 bg-cricket-blue hover:bg-blue-600 rounded-full font-bold transition-colors"
              >
                Play Again
              </button>
            </motion.div>
          ) : (
            <motion.div 
              key="question"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
            >
              <div className="mb-6 flex justify-between items-center text-sm font-semibold text-gray-400">
                <span>Question {currentQuestion + 1} of {quizQuestions.length}</span>
                <span>Score: {score}</span>
              </div>
              
              <h3 className="text-2xl font-bold mb-8 leading-relaxed">
                {quizQuestions[currentQuestion].question}
              </h3>
              
              <div className="space-y-4">
                {quizQuestions[currentQuestion].options.map((option, index) => {
                  let buttonClass = "w-full text-left p-4 rounded-xl border border-white/10 transition-all font-medium flex justify-between items-center ";
                  
                  if (selectedOption === null) {
                    buttonClass += "hover:bg-white/10 bg-white/5 cursor-pointer";
                  } else if (index === quizQuestions[currentQuestion].correctAnswer) {
                    buttonClass += "bg-green-500/20 border-green-500 text-green-400";
                  } else if (index === selectedOption) {
                    buttonClass += "bg-red-500/20 border-red-500 text-red-400";
                  } else {
                    buttonClass += "opacity-50 bg-white/5";
                  }

                  return (
                    <button
                      key={index}
                      onClick={() => handleAnswerClick(index)}
                      className={buttonClass}
                      disabled={selectedOption !== null}
                    >
                      <span>{option}</span>
                      {selectedOption !== null && index === quizQuestions[currentQuestion].correctAnswer && (
                        <CheckCircle2 className="w-5 h-5 text-green-500" />
                      )}
                      {selectedOption === index && index !== quizQuestions[currentQuestion].correctAnswer && (
                        <XCircle className="w-5 h-5 text-red-500" />
                      )}
                    </button>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
