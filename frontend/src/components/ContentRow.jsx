import { motion } from 'framer-motion'
import { Play, Plus, Info, ChevronRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const ContentCard = ({ item }) => {
  const navigate = useNavigate()

  return (
    <motion.div 
      whileHover={{ scale: 1.1, zIndex: 20 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className="relative flex-none w-[200px] md:w-[280px] aspect-video rounded-md overflow-hidden cursor-pointer bg-surface-card group"
      onClick={() => navigate(`/watch/${item.id}/info`)}
    >
      <img 
        src={item.thumbnail} 
        alt={item.title}
        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
      />
      
      {/* Hover Overlay */}
      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-4 flex flex-col justify-end">
        <div className="flex gap-2 mb-3">
          <button 
            onClick={(e) => { e.stopPropagation(); navigate(`/watch/${item.id}`) }}
            className="w-8 h-8 rounded-full bg-white flex items-center justify-center hover:bg-white/80 transition-colors"
          >
            <Play fill="black" size={14} className="text-black ml-0.5" />
          </button>
          <button className="w-8 h-8 rounded-full border border-white/50 flex items-center justify-center hover:border-white transition-colors">
            <Plus size={16} />
          </button>
          <button className="w-8 h-8 rounded-full border border-white/50 flex items-center justify-center ml-auto hover:border-white transition-colors">
            <Info size={16} />
          </button>
        </div>
        <h4 className="text-sm font-bold truncate">{item.title}</h4>
        <div className="flex items-center gap-2 text-[10px] mt-1 text-text-secondary">
          <span className="text-green-500 font-bold">98% Match</span>
          <span className="border border-white/30 px-1 px-0.5">HD</span>
          <span>{item.duration}</span>
        </div>
      </div>
    </motion.div>
  )
}

const ContentRow = ({ title, items }) => {
  return (
    <div className="mb-10 px-4 md:px-12 group/row relative">
      <h3 className="text-xl md:text-2xl font-bold mb-4 text-white/90 hover:text-white transition-colors cursor-pointer flex items-center gap-1 group/title">
        {title} <ChevronRight className="opacity-0 group-hover/title:opacity-100 transition-opacity" size={20} />
      </h3>
      
      <div className="flex gap-4 overflow-x-auto hide-scrollbar pb-8 pt-2 scroll-smooth">
        {items.map((item) => (
          <ContentCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  )
}

export { ContentCard, ContentRow }
