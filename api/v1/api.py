from api.v1.endpoints import messages
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(messages.router, prefix="/task", tags=["BackGround Task Presence Suite"])
