from fastapi import APIRouter

from . import auth, database, query, export, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(database.router, prefix="/database", tags=["database"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(export.router, prefix="/export", tags=["export"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
