from fastapi import APIRouter


from .auth_routes import router as auth_router
from .user_routes import router as user_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=['Auth'])
router.include_router(user_router, prefix="/user", tags=['User'])