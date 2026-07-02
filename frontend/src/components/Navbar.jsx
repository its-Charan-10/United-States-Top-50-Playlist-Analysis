import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Bell, User, Menu, X, Play } from 'lucide-react'
import { clsx } from 'clsx'

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${searchQuery}`)
      setIsSearchOpen(false)
    }
  }

  const navLinks = [
    { name: 'Home', path: '/home' },
    { name: 'TV Shows', path: '/home' },
    { name: 'Movies', path: '/home' },
    { name: 'New & Popular', path: '/home' },
    { name: 'My List', path: '/mylist' },
  ]

  return (
    <nav 
      className={clsx(
        'fixed top-0 w-full z-50 transition-all duration-300 px-4 md:px-12 py-4 flex items-center justify-between',
        isScrolled ? 'bg-surface-overlay/95 backdrop-blur-md border-b border-white/10' : 'bg-gradient-to-b from-black/80 to-transparent'
      )}
    >
      <div className="flex items-center gap-10">
        <Link to="/" className="flex items-center gap-2">
          <span className="text-brand text-3xl font-black tracking-tighter uppercase italic">CineStream</span>
        </Link>

        {/* Desktop Links */}
        <div className="hidden lg:flex items-center gap-6">
          {navLinks.map((link) => (
            <Link 
              key={link.name} 
              to={link.path}
              className="text-sm font-medium text-text-secondary hover:text-white transition-colors"
            >
              {link.name}
            </Link>
          ))}
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="hidden sm:flex items-center gap-4">
          <div className={clsx(
            "flex items-center gap-2 border transition-all duration-300 px-3 py-1.5 rounded-md",
            isSearchOpen ? "w-64 border-white/40 bg-black/40" : "w-10 border-transparent bg-transparent"
          )}>
            <button 
              onClick={() => setIsSearchOpen(!isSearchOpen)}
              className="text-text-secondary hover:text-white transition-colors flex-none"
            >
              <Search size={22} />
            </button>
            {isSearchOpen && (
              <form onSubmit={handleSearch} className="w-full">
                <input 
                  autoFocus
                  type="text"
                  placeholder="Titles, people, genres"
                  className="bg-transparent border-none outline-none text-sm w-full"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </form>
            )}
          </div>
          <button className="text-text-secondary hover:text-white transition-colors">
            <Bell size={22} />
          </button>
          <div 
            onClick={() => navigate('/profile')}
            className="w-8 h-8 rounded-md bg-brand flex items-center justify-center cursor-pointer hover:ring-2 hover:ring-white/20 transition-all"
          >
            <User size={18} className="text-white" />
          </div>
        </div>

        {/* Mobile Menu Toggle */}
        <button 
          className="lg:hidden text-white"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="fixed inset-0 top-[72px] bg-surface-overlay/98 z-40 lg:hidden p-8 flex flex-col gap-8"
        >
          {navLinks.map((link) => (
            <Link 
              key={link.name} 
              to={link.path}
              onClick={() => setIsMobileMenuOpen(false)}
              className="text-xl font-bold hover:text-brand transition-colors"
            >
              {link.name}
            </Link>
          ))}
          <div className="pt-8 border-t border-white/10 flex flex-col gap-6">
             <button className="flex items-center gap-3 text-lg font-medium text-text-secondary">
               <Search /> Search
             </button>
             <button className="flex items-center gap-3 text-lg font-medium text-text-secondary">
               <Bell /> Notifications
             </button>
             <Link 
               to="/profile" 
               className="flex items-center gap-3 text-lg font-medium text-text-secondary"
               onClick={() => setIsMobileMenuOpen(false)}
             >
               <User /> Profile
             </Link>
          </div>
        </motion.div>
      )}
    </nav>
  )
}

export default Navbar
