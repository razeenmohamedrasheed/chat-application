from fastapi import APIRouter
from src.core.models.registraion import Registraion

router = APIRouter(tags=['registration'])


@router.post("/")
async def signup(payload: Registraion):
    try:
        return payload
    except Exception as e:
        return f"error at {e}"
