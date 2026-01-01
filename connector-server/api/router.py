from fastapi import APIRouter


api_router = APIRouter()


@api_router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# TODO: Add other API endpoints
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(database.router, prefix="/database", tags=["database"])
# api_router.include_router(query.router, prefix="/query", tags=["query"])
# api_router.include_router(export.router, prefix="/export", tags=["export"])
# api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
