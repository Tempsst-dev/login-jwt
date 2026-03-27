# ------------------------------    IMPORT MODULES       ------------------------------------------#

import bcrypt
from jose import JWTError , jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()
# ------------------------------    ENV       ------------------------------------------#

SECRET_KEY=os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY not found")

# ------------------------------    HASHED PASSWORD      ------------------------------------------#

def hash_password(password:str):
    Bytes=password.encode("utf-8")
    Salt=bcrypt.gensalt()
    return bcrypt.hashpw(Bytes,Salt).decode("utf-8")
def verf_password(password:str,hashed:str):
    salt= bcrypt.gensalt()
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# ----------------------------------   J . W . T     ------------------------------------------#

def creat_token(data:dict):
    return jwt.encode(data,SECRET_KEY,algorithm="HS256")
def decode_token(token:str):
    try:
        decode= jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return {
    "user_id": decode["user_id"],
    "email": decode["email"]
    }
    except JWTError:
        raise HTTPException(status_code=401,detail="data not found")