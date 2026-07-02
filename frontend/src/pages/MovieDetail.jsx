import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, Plus, Check, ThumbsUp, X } from 'lucide-react'
import { clsx } from 'clsx'
import { ContentRow } from '../components/ContentRow'
import useContentStore from '../store/useContentStore'

const MovieDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { addToWatchlist, removeFromWatchlist, isInWatchlist } = useContentStore()

  const isAdded = isInWatchlist(id)

  // Mock item
  const item = {
    id: id,
    title: 'Interstellar',
    description: 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival. As our time on Earth comes to an end, a team of explorers undertakes the most important mission in human history.',
    genre: ['Sci-Fi', 'Adventure', 'Drama'],
    thumbnail: 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070',
    duration: '2h 49m',
    releaseYear: 2014,
    rating: '8.6',
    cast: ['Matthew McConaughey', 'Anne Hathaway', 'Jessica Chastain']
  }

  return (
    <div className="pt-20 min-h-screen bg-surface-overlay pb-20">
      <div className="relative h-[60vh] md:h-[80vh] w-full">
        <img 
          src={item.thumbnail} 
          className="w-full h-full object-cover"
          alt={item.title}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-surface-overlay via-surface-overlay/20 to-transparent" />
        
        <button 
          onClick={() => navigate(-1)}
          className="absolute top-8 right-8 w-12 h-12 rounded-full bg-black/50 backdrop-blur-md flex items-center justify-center hover:bg-black/80 transition-colors z-20"
        >
          <X size={24} />
        </button>

        <div className="absolute bottom-12 left-4 md:left-12 max-w-3xl z-10">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-6xl font-black mb-6"
          >
            {item.title}
          </motion.h1>
          
          <div className="flex items-center gap-4 mb-8">
            <button 
              onClick={() => navigate(`/watch/${id}`)}
              className="flex items-center gap-2 bg-white text-black px-10 py-3 rounded-md font-bold hover:bg-white/80 transition-all scale-105"
            >
              <Play fill="black" size={20} /> Play
            </button>
            <button 
              onClick={() => isAdded ? removeFromWatchlist(id) : addToWatchlist(item)}
              className={clsx(
                "w-12 h-12 rounded-full border-2 flex items-center justify-center transition-colors",
                isAdded ? "border-green-500 text-green-500 bg-green-500/10" : "border-white/50 text-white hover:border-white"
              )}
            >
              {isAdded ? <Check /> : <Plus />}
            </button>
            <button className="w-12 h-12 rounded-full border-2 border-white/50 flex items-center justify-center hover:border-white transition-colors">
              <ThumbsUp size={20} />
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center gap-4 text-sm font-bold mb-4">
                <span className="text-green-500">98% Match</span>
                <span className="text-text-secondary">{item.releaseYear}</span>
                <span className="border border-white/30 px-1 text-[10px]">13+</span>
                <span className="text-text-secondary">{item.duration}</span>
                <span className="border border-white/30 px-1 text-[10px]">4K</span>
              </div>
              <p className="text-lg text-text-secondary leading-relaxed mb-6">
                {item.description}
              </p>
            </div>

            <div className="flex flex-col gap-4 text-sm">
              <div>
                <span className="text-text-muted">Cast:</span> {item.cast.join(', ')}
              </div>
              <div>
                <span className="text-text-muted">Genres:</span> {item.genre.join(', ')}
              </div>
              <div>
                <span className="text-text-muted">This movie is:</span> Mind-bending, Epic, Emotional
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <ContentRow title="More Like This" items={[]} />
      </div>
    </div>
  )
}

export default MovieDetail
