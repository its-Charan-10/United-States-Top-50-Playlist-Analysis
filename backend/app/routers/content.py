from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from ..models.schemas import Content
from ..services.firebase_service import firebase_service
from ..middleware.auth import verify_token

router = APIRouter()

@router.get("/", response_model=List[Content])
async def get_all_content(genre: str = None):
    try:
        content = await firebase_service.get_content(genre)
        # If DB is empty, return empty list or fallback to mock
        return content
    except Exception as e:
        # Fallback for dev environment without valid Firebase config
        return []

@router.get("/trending", response_model=List[Content])
async def get_trending():
    return await firebase_service.get_trending()

@router.get("/{content_id}", response_model=Content)
async def get_content_by_id(content_id: str):
    content_ref = firebase_service.db.collection('content').document(content_id).get()
    if not content_ref.exists:
        raise HTTPException(status_code=404, detail="Content not found")
    return {**content_ref.to_dict(), "id": content_ref.id}

@router.post("/watchlist/{action}")
async def update_watchlist(content_id: str, action: str, user=Depends(verify_token)):
    if action not in ["add", "remove"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    await firebase_service.update_user_watchlist(user['uid'], content_id, action)
    return {"status": "success"}

@router.get("/search", response_model=List[Content])
async def search_content(q: str = Query(...)):
    all_content = await firebase_service.get_content()
    return [c for c in all_content if q.lower() in c["title"].lower()]

@router.get("/recommendations/{content_id}", response_model=List[Content])
async def get_recommendations(content_id: str):
    target = await get_content_by_id(content_id)
    all_content = await firebase_service.get_content()
    recommendations = [
        c for c in all_content 
        if c['id'] != content_id and any(g in target['genre'] for g in c['genre'])
    ]
    return recommendations[:6]
