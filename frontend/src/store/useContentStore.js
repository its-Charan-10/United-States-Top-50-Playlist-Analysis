import { create } from 'zustand'
import axios from 'axios'

const useContentStore = create((set, get) => ({
  trending: [],
  popular: [],
  searchResults: [],
  watchlist: [],
  loading: false,
  error: null,

  fetchTrending: async () => {
    set({ loading: true })
    try {
      const { data } = await axios.get('/api/content/trending')
      set({ trending: data, loading: false })
    } catch (err) {
      set({ error: err.message, loading: false })
    }
  },

  search: async (query) => {
    if (!query) return set({ searchResults: [] })
    set({ loading: true })
    try {
      const { data } = await axios.get(`/api/content/search?q=${query}`)
      set({ searchResults: data, loading: false })
    } catch (err) {
      set({ error: err.message, loading: false })
    }
  },

  addToWatchlist: (item) => {
    const { watchlist } = get()
    if (!watchlist.find(i => i.id === item.id)) {
      set({ watchlist: [...watchlist, item] })
    }
  },

  removeFromWatchlist: (itemId) => {
    const { watchlist } = get()
    set({ watchlist: watchlist.filter(i => i.id !== itemId) })
  },
  
  isInWatchlist: (itemId) => {
    return get().watchlist.some(i => i.id === itemId)
  }
}))

export default useContentStore
