import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import LevelSelect from './pages/LevelSelect';
import QuizGame from './pages/QuizGame';
import Results from './pages/Results';
import Header from './components/Header';

function App() {
  const [screen, setScreen] = useState('home'); // 'home' | 'quiz' | 'results'
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [quizResult, setQuizResult] = useState(null);
  const [completedLevels, setCompletedLevels] = useState([]);

  const startQuiz = (level) => {
    setSelectedLevel(level);
    setScreen('quiz');
  };

  const finishQuiz = (result) => {
    setQuizResult(result);
    if (result.percentage >= 60 && !completedLevels.includes(result.level)) {
      setCompletedLevels(prev => [...prev, result.level]);
    }
    setScreen('results');
  };

  const goHome = () => {
    setScreen('home');
    setSelectedLevel(null);
    setQuizResult(null);
  };

  const retryQuiz = () => {
    setScreen('quiz');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header onLogoClick={goHome} />
      <main className="flex-grow">
        <AnimatePresence mode="wait">
          {screen === 'home' && (
            <LevelSelect
              key="home"
              onSelectLevel={startQuiz}
              completedLevels={completedLevels}
            />
          )}
          {screen === 'quiz' && selectedLevel && (
            <QuizGame
              key={`quiz-${selectedLevel}`}
              level={selectedLevel}
              onFinish={finishQuiz}
              onQuit={goHome}
            />
          )}
          {screen === 'results' && quizResult && (
            <Results
              key="results"
              result={quizResult}
              onRetry={retryQuiz}
              onHome={goHome}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
