import { useEffect } from 'react'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import Watch from './pages/Watch'
import MovieDetail from './pages/MovieDetail'
import Search from './pages/Search'
import MyList from './pages/MyList'
import Profile from './pages/Profile'
import AdminDashboard from './pages/AdminDashboard'
import useAuthStore from './store/useAuthStore'

function App() {
  const { user, loading, init } = useAuthStore()
  const location = useLocation()

  useEffect(() => {
    init()
  }, [init])

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-surface-overlay">
        <div className="text-brand text-5xl font-black italic animate-pulse">CineStream</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-surface-overlay text-white font-sans selection:bg-brand selection:text-white">
      <Navbar />
      <main className="min-h-[calc(100vh-200px)]">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={user ? <Navigate to="/home" /> : <Landing />} />
            <Route path="/home" element={user ? <Home /> : <Navigate to="/login" />} />
            <Route path="/login" element={!user ? <Login /> : <Navigate to="/home" />} />
            <Route path="/register" element={!user ? <Register /> : <Navigate to="/home" />} />
            <Route path="/watch/:id" element={user ? <Watch /> : <Navigate to="/login" />} />
            <Route path="/watch/:id/info" element={user ? <MovieDetail /> : <Navigate to="/login" />} />
            <Route path="/search" element={user ? <Search /> : <Navigate to="/login" />} />
            <Route path="/mylist" element={user ? <MyList /> : <Navigate to="/login" />} />
            <Route path="/profile" element={user ? <Profile /> : <Navigate to="/login" />} />
            <Route path="/admin" element={user ? <AdminDashboard /> : <Navigate to="/login" />} />
          </Routes>
        </AnimatePresence>
      </main>
      <Footer />
    </div>
  )
}

export default App
