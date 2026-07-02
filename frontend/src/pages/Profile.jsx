import { motion } from 'framer-motion'
import useAuthStore from '../store/useAuthStore'
import { LogOut, CreditCard, Shield, Settings, User } from 'lucide-react'
import { toast } from 'react-hot-toast'

const Profile = () => {
  const { user, logout } = useAuthStore()

  const handleLogout = async () => {
    try {
      await logout()
      toast.success('Signed out successfully')
    } catch (err) {
      toast.error(err.message)
    }
  }

  const sections = [
    { icon: <CreditCard />, title: 'Membership & Billing', action: 'Manage Plan' },
    { icon: <Shield />, title: 'Security & Privacy', action: 'Update Password' },
    { icon: <Settings />, title: 'Parental Controls', action: 'Configure' },
  ]

  return (
    <div className="pt-24 min-h-screen px-4 md:px-12 bg-surface-overlay">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-black mb-10">Account</h1>

        {/* Profile Card */}
        <div className="glass-card p-8 rounded-2xl mb-8 flex flex-col md:flex-row items-center gap-8">
          <div className="w-24 h-24 rounded-lg bg-brand flex items-center justify-center text-4xl font-bold">
            {user?.email?.[0].toUpperCase() || 'U'}
          </div>
          <div className="flex-1 text-center md:text-left">
            <h2 className="text-2xl font-bold mb-1">{user?.email}</h2>
            <p className="text-text-secondary mb-4">Member since May 2026</p>
            <div className="flex flex-wrap gap-2 justify-center md:justify-start">
              <span className="bg-brand/20 text-brand px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Premium Plan</span>
              <span className="bg-white/10 text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">4K Streaming</span>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="flex items-center gap-2 bg-white/10 hover:bg-white/20 px-6 py-2 rounded-md font-bold transition-all text-red-500"
          >
            <LogOut size={20} /> Sign Out
          </button>
        </div>

        {/* Settings List */}
        <div className="space-y-4">
          {sections.map((section, idx) => (
            <motion.div 
              key={idx}
              whileHover={{ x: 5 }}
              className="glass-card p-6 rounded-xl flex items-center justify-between group cursor-pointer"
            >
              <div className="flex items-center gap-4 text-text-secondary group-hover:text-white transition-colors">
                <div className="p-2 bg-white/5 rounded-lg">{section.icon}</div>
                <span className="font-medium">{section.title}</span>
              </div>
              <button className="text-brand font-bold text-sm hover:underline">
                {section.action}
              </button>
            </motion.div>
          ))}
        </div>

        {/* Admin Link (Conditional) */}
        <div className="mt-12 p-8 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center text-center">
          <Shield className="text-text-muted mb-4" size={32} />
          <h3 className="text-xl font-bold mb-2">Internal Tools</h3>
          <p className="text-text-secondary mb-6 max-w-sm">Access the CineStream content management system to upload and manage the movie library.</p>
          <button 
             onClick={() => navigate('/admin')}
             className="bg-white text-black px-8 py-2 rounded-md font-bold hover:bg-white/80 transition-all"
          >
            Go to Admin Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}

export default Profile
