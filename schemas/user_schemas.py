# ------------------------------    INPORT MODULE       ------------------------------------------#

from pydantic import BaseModel,EmailStr
# ------------------------------   REGISTER MODELS DATA     ------------------------------------------#

class Data(BaseModel):
    name:str
    lastname:str
    email:EmailStr
    password:str

# ------------------------------   LOGIN MODELS DATA     ------------------------------------------#

class Login_data(BaseModel):
    email:EmailStr
    password:str