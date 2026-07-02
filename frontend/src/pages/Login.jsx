import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import useAuthStore from '../store/useAuthStore'
import { toast } from 'react-hot-toast'
import { Mail, Lock, ChevronRight } from 'lucide-react'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { login, loginWithGoogle } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      await login(email, password)
      toast.success('Welcome back!')
      navigate('/home')
    } catch (err) {
      toast.error(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleGoogleLogin = async () => {
    try {
      await loginWithGoogle()
      toast.success('Signed in with Google')
      navigate('/home')
    } catch (err) {
      toast.error(err.message)
    }
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 pt-20">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img 
          src="https://images.unsplash.com/photo-1574267432553-4b4628081c31?q=80&w=2062&auto=format&fit=crop" 
          className="w-full h-full object-cover opacity-30 grayscale"
          alt="Login Background"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-surface-overlay via-surface-overlay/80 to-surface-overlay" />
      </div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="relative z-10 w-full max-w-md p-8 md:p-12 glass-card rounded-2xl shadow-2xl"
      >
        <h2 className="text-3xl font-black mb-8 text-center">Sign In</h2>
        
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-sm text-text-secondary ml-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
              <input 
                type="email" 
                required
                className="w-full bg-white/5 border border-white/10 rounded-lg py-3 pl-10 pr-4 outline-none focus:border-brand transition-colors"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-sm text-text-secondary ml-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
              <input 
                type="password" 
                required
                className="w-full bg-white/5 border border-white/10 rounded-lg py-3 pl-10 pr-4 outline-none focus:border-brand transition-colors"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full bg-brand hover:bg-brand-dark text-white font-bold py-3 rounded-lg mt-2 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Signing in...' : 'Sign In'} <ChevronRight size={20} />
          </button>
        </form>

        <div className="my-8 flex items-center gap-4 text-text-muted">
          <div className="flex-1 h-px bg-white/10" />
          <span className="text-xs uppercase font-bold">OR</span>
          <div className="flex-1 h-px bg-white/10" />
        </div>

        <button 
          onClick={handleGoogleLogin}
          className="w-full bg-white text-black font-bold py-3 rounded-lg flex items-center justify-center gap-3 hover:bg-white/90 transition-all"
        >
          <img src="https://www.google.com/favicon.ico" className="w-5 h-5" alt="Google" />
          Continue with Google
        </button>

        <button 
          onClick={() => {
            setEmail('demo@example.com');
            setPassword('password123');
            toast.success('Demo credentials loaded. Click Sign In.');
          }}
          className="w-full bg-white/10 text-white font-bold py-3 rounded-lg flex items-center justify-center gap-3 hover:bg-white/20 transition-all mt-4 border border-white/10"
        >
          Use Demo Account
        </button>

        <div className="mt-8 text-center text-text-secondary">
          New to CineStream? <Link to="/register" className="text-white hover:underline">Sign up now.</Link>
        </div>
      </motion.div>
    </div>
  )
}

export default Login
