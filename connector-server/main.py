from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.config import settings
from api.router import api_router

app = FastAPI(
    title="Database Connector API",
    description="Secure API for database operations",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root API endpoint providing server information and navigation links.
    """
    return {
        "name": "Database Connector API Server",
        "version": "1.0.0",
        "description": "Production-ready database connector with MySQL, Redis, FastAPI",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "api_health": "/api/v1/health"
        },
        "services": {
            "mysql": {
                "host": "localhost",
                "port": 3307,
                "database": "connector_db"
            },
            "redis": {
                "host": "localhost",
                "port": 6380
            },
            "api": {
                "host": "localhost",
                "port": 3003
            }
        },
        "features": [
            "JWT Authentication",
            "API Key Management",
            "Rate Limiting",
            "CORS Protection",
            "SQL Injection Prevention"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.debug,
    )
