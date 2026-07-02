import { motion } from 'framer-motion'
import { Play, Info, ChevronRight, ChevronLeft } from 'lucide-react'
import { Link } from 'react-router-dom'
import { clsx } from 'clsx'

const Landing = () => {
  return (
    <div className="relative min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[100vh] w-full overflow-hidden">
        {/* Mock Background Image/Video */}
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop" 
            alt="Hero Background" 
            className="w-full h-full object-cover brightness-50"
          />
          <div className="absolute inset-0 hero-gradient" />
          <div className="absolute inset-0 bg-gradient-to-t from-surface-overlay via-transparent to-transparent" />
        </div>

        <div className="relative z-10 h-full flex flex-col justify-center px-4 md:px-12 max-w-2xl">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-black mb-4 leading-tight">
              INTERSTELLAR
            </h1>
            <p className="text-lg md:text-xl text-text-secondary mb-8 line-clamp-3">
              A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. A cinematic masterpiece that redefines time and space.
            </p>

            <div className="flex flex-wrap gap-4">
              <Link 
                to="/login"
                className="flex items-center gap-2 bg-white text-black px-8 py-3 rounded-md font-bold hover:bg-white/80 transition-colors"
              >
                <Play fill="black" size={20} /> Play
              </Link>
              <button className="flex items-center gap-2 bg-white/20 text-white px-8 py-3 rounded-md font-bold hover:bg-white/30 transition-colors backdrop-blur-md">
                <Info size={20} /> More Info
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature Sections */}
      <section className="py-20 px-4 md:px-12 bg-surface-overlay">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl md:text-5xl font-black mb-6">Enjoy on your TV.</h2>
            <p className="text-xl text-text-secondary">
              Watch on Smart TVs, Playstation, Xbox, Chromecast, Apple TV, Blu-ray players and more.
            </p>
          </div>
          <div className="relative rounded-2xl overflow-hidden shadow-2xl shadow-brand/10">
            <img 
              src="https://images.unsplash.com/photo-1593359677759-543733fbd9c3?q=80&w=2070&auto=format&fit=crop" 
              alt="TV Feature" 
              className="w-full aspect-video object-cover"
            />
            <div className="absolute inset-0 border-2 border-white/10 rounded-2xl pointer-events-none" />
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-4 md:px-12 bg-surface">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-black mb-4">Choose the plan that's right for you.</h2>
          <p className="text-text-secondary">Downgrade or upgrade at any time.</p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            { name: 'Basic', price: '8.99', quality: '720p', screens: 1 },
            { name: 'Standard', price: '13.99', quality: '1080p', screens: 2, recommended: true },
            { name: 'Premium', price: '17.99', quality: '4K+HDR', screens: 4 },
          ].map((plan) => (
            <motion.div 
              key={plan.name}
              whileHover={{ y: -10 }}
              className={clsx(
                "glass-card p-8 rounded-2xl flex flex-col items-center text-center",
                plan.recommended ? "border-brand border-2 scale-105" : "border-white/5"
              )}
            >
              {plan.recommended && (
                <span className="bg-brand text-xs font-bold px-3 py-1 rounded-full mb-4 uppercase tracking-wider">
                  Recommended
                </span>
              )}
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-4xl font-black">${plan.price}</span>
                <span className="text-text-muted">/month</span>
              </div>
              <ul className="flex flex-col gap-4 mb-10 text-text-secondary w-full">
                <li className="flex justify-between border-b border-white/5 pb-2">
                  <span>Resolution</span>
                  <span className="text-white font-medium">{plan.quality}</span>
                </li>
                <li className="flex justify-between border-b border-white/5 pb-2">
                  <span>Simultaneous screens</span>
                  <span className="text-white font-medium">{plan.screens}</span>
                </li>
                <li className="flex justify-between border-b border-white/5 pb-2">
                  <span>Cancel anytime</span>
                  <span className="text-white font-medium">Yes</span>
                </li>
              </ul>
              <Link 
                to="/register" 
                className={clsx(
                  "w-full py-3 rounded-md font-bold transition-all",
                  plan.recommended ? "bg-brand text-white hover:bg-brand-dark" : "bg-white/10 text-white hover:bg-white/20"
                )}
              >
                Choose {plan.name}
              </Link>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Landing
