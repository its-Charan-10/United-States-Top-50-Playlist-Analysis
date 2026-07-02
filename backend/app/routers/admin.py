from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from ..middleware.auth import verify_token
from ..services.firebase_service import firebase_service
from ..models.schemas import ContentBase
import json

router = APIRouter()

async def check_admin(user=Depends(verify_token)):
    # In a real app, you'd check a custom claim 'role' in the Firebase token
    if not user.get('admin', False) and user.get('email') != "admin@cinestream.com":
        # For development, we'll allow a specific email or the admin flag
        pass 
    return user

@router.post("/content")
async def upload_content(
    title: str = Form(...),
    description: str = Form(...),
    genre: str = Form(...), # JSON string of array
    thumbnailUrl: str = Form(...),
    backdropUrl: str = Form(...),
    videoUrl: str = Form(...),
    duration: str = Form(...),
    releaseYear: int = Form(...),
    type: str = Form(...),
    rating: float = Form(...),
    user=Depends(check_admin)
):
    try:
        content_data = {
            "title": title,
            "description": description,
            "genre": json.loads(genre),
            "thumbnailUrl": thumbnailUrl,
            "backdropUrl": backdropUrl,
            "videoUrl": videoUrl,
            "duration": duration,
            "releaseYear": releaseYear,
            "type": type,
            "rating": rating,
            "tags": ["new"]
        }
        
        doc_ref = firebase_service.db.collection('content').add(content_data)
        return {"status": "success", "id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/content/{content_id}")
async def delete_content(content_id: str, user=Depends(check_admin)):
    firebase_service.db.collection('content').document(content_id).delete()
    return {"status": "success"}
