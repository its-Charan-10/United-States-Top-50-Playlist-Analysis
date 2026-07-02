import { create } from 'zustand'
import { auth } from '../services/firebase'
import { 
  onAuthStateChanged, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut,
  GoogleAuthProvider,
  signInWithPopup
} from 'firebase/auth'

const useAuthStore = create((set) => ({
  user: null,
  loading: true,
  error: null,

  setUser: (user) => set({ user, loading: false }),
  
  init: () => {
    onAuthStateChanged(auth, (user) => {
      set({ user, loading: false })
    })
  },

  login: async (email, password) => {
    set({ loading: true, error: null })
    try {
      // Dev bypass for specific email
      if (email === 'demo@example.com' && password === 'password123') {
        set({ user: { email, uid: 'dev-user-123' }, loading: false })
        return
      }
      await signInWithEmailAndPassword(auth, email, password)
    } catch (err) {
      set({ error: err.message, loading: false })
      throw err
    }
  },

  guestLogin: () => {
    set({ user: { email: 'guest@cinestream.com', uid: 'guest-uid' }, loading: false })
  },

  register: async (email, password) => {
    set({ loading: true, error: null })
    try {
      await createUserWithEmailAndPassword(auth, email, password)
    } catch (err) {
      set({ error: err.message, loading: false })
      throw err
    }
  },

  loginWithGoogle: async () => {
    set({ loading: true, error: null })
    try {
      const provider = new GoogleAuthProvider()
      await signInWithPopup(auth, provider)
    } catch (err) {
      set({ error: err.message, loading: false })
      throw err
    }
  },

  logout: async () => {
    await signOut(auth)
    set({ user: null })
  },
}))

export default useAuthStore
