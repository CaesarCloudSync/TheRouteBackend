from pydantic import BaseModel

class AuthModel(BaseModel):
    email:str
    password:str