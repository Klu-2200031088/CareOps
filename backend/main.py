from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from app.routes import auth, workspace, contacts, bookings, inbox, dashboard, forms, inventory

# Initialize database
from app.database import engine, Base

# Create tables - THIS MUST RUN BEFORE APP STARTS
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized")
except Exception as e:
    print(f"❌ Database initialization error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 CareOps Backend Starting...")
    yield
    # Shutdown
    print("🛑 CareOps Backend Shutting Down...")

app = FastAPI(
    title="CareOps API",
    description="Unified Operations Platform for Service Businesses",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration - Accept all Vercel preview deployments, localhost, and env-configured origins
cors_regex = r"https://.*\.vercel\.app|http://localhost:\d+"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(workspace.router, prefix="/api/workspace", tags=["workspace"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(inbox.router, prefix="/api/inbox", tags=["inbox"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(forms.router, prefix="/api/forms", tags=["forms"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])

@app.get("/")
async def root():
    return {
        "message": "🎯 CareOps API - Unified Operations Platform",
        "version": "0.1.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
