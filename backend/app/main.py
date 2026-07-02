# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials

load_dotenv()

# Initialize Firebase Admin
try:
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccount.json")
    if os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    else:
        # Try default initialization
        try:
            firebase_admin.initialize_app()
        except Exception:
            print("Firebase Admin could not be initialized. Backend will run in limited mode.")
except Exception as e:
    print(f"Firebase Admin error: {e}")

app = FastAPI(
    title="CineStream API",
    description="Scalable backend for cinematic streaming platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CineStream API is online", "status": "healthy"}

from .routers import content, subscriptions, admin

# Include routers
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
