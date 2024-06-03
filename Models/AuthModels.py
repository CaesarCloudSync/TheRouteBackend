from pydantic import BaseModel

class AuthModel(BaseModel):
    email:str
    password:str
    first_name:str
    last_name:str
    date_of_birth:str