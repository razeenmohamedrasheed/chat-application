from fastapi import APIRouter, status
from src.core.models.registraion import Registraion
from src.utilities.database import Database
from passlib.context import CryptContext
import logging

router = APIRouter(tags=['registration'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def signup(payload: Registraion):
    try:
        db = Database()
        columns = ['username', 'email', 'contact', 'dob', 'hashed_password', 'gender', 'roleid']
        hashed_password = pwd_context.hash(payload.password)
        values = [
            payload.name,
            payload.email,
            payload.contact,
            payload.dob,
            hashed_password,
            payload.gender,
            payload.roleid
        ]
        db.insert_query('users', columns, values, auto_commit=True)
        return "Registration Success"
    except Exception as e:
        logging.error(f"Signup failed: {e}")
        return {"error": "Registration failed. Please try again later."}
