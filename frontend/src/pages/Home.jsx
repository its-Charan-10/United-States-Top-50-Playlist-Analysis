import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Play, Info, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ContentRow } from '../components/ContentRow'

import useContentStore from '../store/useContentStore'

const Home = () => {
  const { trending, fetchTrending, loading } = useContentStore()

  useEffect(() => {
    fetchTrending()
  }, [fetchTrending])

  // Mock Data fallback
  const fallbackMovies = [
    { id: 1, title: 'Stranger Things', thumbnail: 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070', duration: '45m' },
    { id: 2, title: 'The Witcher', thumbnail: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1925', duration: '50m' },
  ]

  const movies = trending.length > 0 ? trending : fallbackMovies

  return (
    <div className="pb-20 overflow-x-hidden">
      {/* Featured Banner */}
      <section className="relative h-[80vh] w-full mb-[-50px]">
        <div className="absolute inset-0">
          <img 
            src="https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070" 
            className="w-full h-full object-cover"
            alt="Featured"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-surface-overlay via-surface-overlay/40 to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-surface-overlay via-transparent to-transparent" />
        </div>

        <div className="relative z-10 h-full flex flex-col justify-center px-4 md:px-12 max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="flex items-center gap-2 mb-4">
              <span className="text-brand text-2xl font-black italic">N</span>
              <span className="text-text-secondary font-bold tracking-widest text-xs uppercase">Series</span>
            </span>
            <h1 className="text-5xl md:text-7xl font-black mb-4 leading-tight">ARCANE</h1>
            <p className="text-lg text-text-secondary mb-8 line-clamp-3">
              Amidst the escalating unrest between the rich city of Piltover and the seedy underbelly of Zaun, two sisters fight on opposite sides of a war between magic technologies and clashing convictions.
            </p>

            <div className="flex gap-4">
              <Link to="/watch/featured" className="flex items-center gap-2 bg-white text-black px-8 py-2.5 rounded-md font-bold hover:bg-white/80 transition-colors">
                <Play fill="black" size={20} /> Play
              </Link>
              <button className="flex items-center gap-2 bg-white/20 text-white px-8 py-2.5 rounded-md font-bold hover:bg-white/30 transition-colors backdrop-blur-md">
                <Info size={20} /> More Info
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Rows */}
      <div className="relative z-10 space-y-12">
        <ContentRow title="Trending Now" items={mockMovies} />
        <ContentRow title="New Releases" items={[...mockMovies].reverse()} />
        <ContentRow title="Popular on CineStream" items={mockMovies.slice(2).concat(mockMovies.slice(0, 2))} />
        <ContentRow title="Action Movies" items={mockMovies} />
        <ContentRow title="Sci-Fi Series" items={mockMovies} />
      </div>
    </div>
  )
}

export default Home
