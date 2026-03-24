from fastapi import APIRouter

from app.api.routes import (
    admin_auth,
    admin_geocoding,
    admin_imports,
    admin_locations,
    admin_store_configs,
    health,
    public_locations,
    public_store_config,
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
api_router.include_router(
    admin_store_configs.router,
    prefix="/admin/store-configs",
    tags=["admin-store-configs"],
)
api_router.include_router(admin_imports.router, prefix="/admin/imports", tags=["admin-imports"])
api_router.include_router(
    admin_geocoding.router,
    prefix="/admin/geocoding",
    tags=["admin-geocoding"],
)
api_router.include_router(
    public_locations.router,
    prefix="/public/locations",
    tags=["public-locations"],
)
api_router.include_router(
    public_store_config.router,
    prefix="/public/store-config",
    tags=["public-store-config"],
)
api_router.include_router(taxonomy.router, prefix="/taxonomy", tags=["taxonomy"])
