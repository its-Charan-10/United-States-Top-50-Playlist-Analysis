import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import os
from typing import List, Optional

class FirebaseService:
    def __init__(self):
        self.mock_content = [
            {
                "id": "featured",
                "title": "Arcane",
                "description": "Amidst the escalating unrest between the rich city of Piltover and the seedy underbelly of Zaun, two sisters fight on opposite sides of a war between magic technologies and clashing convictions.",
                "genre": ["Sci-Fi", "Action", "Adventure"],
                "thumbnailUrl": "https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070",
                "backdropUrl": "https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070",
                "videoUrl": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
                "duration": "42m",
                "releaseYear": 2021,
                "type": "series",
                "rating": 9.0,
                "tags": ["trending", "popular"]
            },
            {
                "id": "interstellar",
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "genre": ["Sci-Fi", "Drama"],
                "thumbnailUrl": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070",
                "backdropUrl": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070",
                "videoUrl": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
                "duration": "2h 49m",
                "releaseYear": 2014,
                "type": "movie",
                "rating": 8.6,
                "tags": ["popular"]
            }
        ]
        try:
            self.db = firestore.client()
            self.bucket = storage.bucket()
            self.initialized = True
        except Exception as e:
            print(f"Firestore/Storage client error: {e}")
            self.db = None
            self.bucket = None
            self.initialized = False

    async def get_content(self, genre: Optional[str] = None) -> List[dict]:
        if not self.db: 
            if genre:
                return [c for c in self.mock_content if genre.lower() in [g.lower() for g in c['genre']]]
            return self.mock_content
        content_ref = self.db.collection('content')
        if genre:
            query = content_ref.where('genre', 'array_contains', genre)
            docs = query.stream()
        else:
            docs = content_ref.stream()
        
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    async def get_trending(self, limit: int = 10) -> List[dict]:
        if not self.db: 
            return [c for c in self.mock_content if 'trending' in c.get('tags', [])][:limit]
        docs = self.db.collection('content').where('tags', 'array_contains', 'trending').limit(limit).stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    async def update_user_watchlist(self, uid: str, content_id: str, action: str):
        if not self.db: return
        user_ref = self.db.collection('users').document(uid)
        if action == "add":
            user_ref.update({"watchlist": firestore.ArrayUnion([content_id])})
        else:
            user_ref.update({"watchlist": firestore.ArrayRemove([content_id])})

    async def get_user_profile(self, uid: str) -> dict:
        if not self.db: return None
        doc = self.db.collection('users').document(uid).get()
        return doc.to_dict() if doc.exists else None

firebase_service = FirebaseService()
