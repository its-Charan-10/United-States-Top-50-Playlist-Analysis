import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';

// Pages
import Home from './pages/Home';
import LiveScores from './pages/LiveScores';
import Teams from './pages/Teams';
import Players from './pages/Players';
import MatchCenter from './pages/MatchCenter';
import Quiz from './pages/Quiz';
import FunZone from './pages/FunZone';
import Gallery from './pages/Gallery';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navigation />
        <main className="flex-grow pt-20">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scores" element={<LiveScores />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/players" element={<Players />} />
            <Route path="/matches" element={<MatchCenter />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/funzone" element={<FunZone />} />
            <Route path="/gallery" element={<Gallery />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
