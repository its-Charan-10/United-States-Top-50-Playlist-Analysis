import { motion } from 'framer-motion'
import useContentStore from '../store/useContentStore'
import { ContentCard } from '../components/ContentRow'
import { Link } from 'react-router-dom'

const MyList = () => {
  const { watchlist } = useContentStore()

  return (
    <div className="pt-24 min-h-screen px-4 md:px-12 bg-surface-overlay">
      <h1 className="text-3xl font-black mb-10">My List</h1>

      {watchlist.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-x-4 gap-y-12">
          {watchlist.map((item) => (
            <ContentCard key={item.id} item={item} />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-40 text-center">
          <p className="text-xl text-text-muted mb-6">You haven't added anything to your list yet.</p>
          <Link 
            to="/home" 
            className="bg-white text-black px-8 py-2 rounded-md font-bold hover:bg-white/80 transition-all"
          >
            Explore Movies
          </Link>
        </div>
      )}
    </div>
  )
}

export default MyList
