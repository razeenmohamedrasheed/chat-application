from fastapi import APIRouter, status
from src.core.models.registraion import Registraion, Login
from src.utilities.database import Database
from passlib.context import CryptContext
from src.utilities.utils import verify_password
from datetime import datetime, timedelta, timezone
import logging

router = APIRouter(tags=['registration'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=status.HTTP_201_CREATED)
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

@router.post("/login")
async def Login(payload:Login):
    # try:
        db = Database()
        users = db.select_query("users")
        print(users)
        for user in users:
            if user['username'] != payload.name:
                return "Incorrect Username"
            if not verify_password(payload.password, user['hashed_password']):
                return "Incorrect Password"
    # except Exception as e:
    #     logging.error(f"Signup failed: {e}")
    #     return {"error": "Login failed. Please try again later."}

