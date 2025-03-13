from fastapi import APIRouter

from app.api.endpoints import auth, translation, dictionary, parameters

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(translation.router, prefix="/translation", tags=["translation"])
api_router.include_router(dictionary.router, prefix="/dictionary", tags=["dictionary"])
api_router.include_router(parameters.router, prefix="/parameters", tags=["parameters"])
