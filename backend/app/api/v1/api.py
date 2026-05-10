from fastapi import APIRouter

from .endpoints import admin, experience, posts, projects

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(experience.router, prefix="/experience", tags=["experience"])
