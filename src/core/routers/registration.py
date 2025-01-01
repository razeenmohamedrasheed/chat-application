from fastapi import APIRouter
from src.core.models.registraion import Registraion

router = APIRouter(tags=['registration'])


@router.post("/")
def signup(payload: Registraion):
    return payload
