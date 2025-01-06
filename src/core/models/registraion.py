from pydantic import BaseModel


class Registraion(BaseModel):
    name: str
    email: str
    contact: str
    dob: str
    password: str
    gender: str
    roleid:int

class Login(BaseModel):
    name:str
    password:str
