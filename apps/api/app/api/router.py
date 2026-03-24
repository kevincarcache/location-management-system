from fastapi import APIRouter

from app.api.routes import (
    admin_auth,
    admin_imports,
    admin_locations,
    health,
    public_locations,
    taxonomy,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(admin_auth.router, prefix="/admin/auth", tags=["admin-auth"])
api_router.include_router(
    admin_locations.router,
    prefix="/admin/locations",
    tags=["admin-locations"],
)
api_router.include_router(admin_imports.router, prefix="/admin/imports", tags=["admin-imports"])
api_router.include_router(
    public_locations.router,
    prefix="/public/locations",
    tags=["public-locations"],
)
api_router.include_router(taxonomy.router, prefix="/taxonomy", tags=["taxonomy"])
