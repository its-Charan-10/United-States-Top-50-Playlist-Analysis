import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import useContentStore from '../store/useContentStore'
import { ContentCard } from '../components/ContentRow'

const Search = () => {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q')
  const { searchResults, search, loading } = useContentStore()

  useEffect(() => {
    if (query) {
      search(query)
    }
  }, [query, search])

  return (
    <div className="pt-24 min-h-screen px-4 md:px-12 bg-surface-overlay">
      <h2 className="text-2xl text-text-secondary mb-8">
        Search results for: <span className="text-white font-bold">{query}</span>
      </h2>

      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {[1,2,3,4,5,6].map(i => (
            <div key={i} className="aspect-video bg-surface-card rounded-md skeleton" />
          ))}
        </div>
      ) : searchResults.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-x-4 gap-y-12">
          {searchResults.map((item) => (
            <ContentCard key={item.id} item={item} />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <p className="text-xl text-text-muted">Your search for "{query}" did not have any matches.</p>
          <ul className="mt-4 text-text-muted text-sm list-disc list-inside">
            <li>Try different keywords</li>
            <li>Looking for a movie or TV show?</li>
            <li>Try using a movie title or actor's name</li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default Search
