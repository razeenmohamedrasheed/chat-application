from fastapi import APIRouter, status
from src.core.models.registraion import Registraion,Login
from src.utilities.database import Database
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import logging

router = APIRouter(tags=['registration'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "e3731f12f9e32738efe17fd94ec6dff8ab894b08b558225e01b7b2e3c9bf783a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def generate_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    print(expires_delta)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@router.post('/login')
def login(payload:Login):
    if payload.username != "razeen":
        return "Incorrect Username"
    elif payload.password != "razeen@123":
        return "Incorrect Password"
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = generate_access_token(data={"sub": payload.username}, expires_delta=access_token_expires)
        return access_token
