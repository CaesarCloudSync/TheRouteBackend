from pydantic import BaseModel

class SignupAuthModel(BaseModel):
    email:str
    password:str
    first_name:str
    last_name:str
    date_of_birth:str
class LoginAuthModel(BaseModel):
    email:str
    password:str