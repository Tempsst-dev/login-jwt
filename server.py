# ------------------------------    IMPORT MODULES       ------------------------------------------#

from fastapi import FastAPI , Header,HTTPException,Query
from pydantic import BaseModel,EmailStr
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from jose import JWTError , jwt
from datetime import datetime,timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ------------------------------ CORSMiddleware  ------------------------------------------#
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------ server start  ------------------------------------------#

@app.get("/")
async def root():
    return {"server":"start"}

# ------------------------------  VARIABLE   ------------------------------------------#
load_dotenv()
# ===== DATA BASE=====
URL=os.getenv("URL")
CLIENT=MongoClient(URL)
CREAT_USERS=CLIENT["CREAT_USERS"]
USER_DATA=CREAT_USERS["USER_DATA"]

# =========== J.W.T ==============

SECRET_KEY=os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY not found")
# ----------------CALSS DATA-------------------
class Data(BaseModel):
    name:str
    lastname:str
    email:EmailStr
    password:str
# ---------------------------------  DATA BASE CONECTE   ---------------------------------#
@app.post("/register")
async def register(data:Data):
    password= data.password
    Bytes=password.encode("utf-8")
    Salt=bcrypt.gensalt()
    hash=bcrypt.hashpw(Bytes,Salt)
    regester_data={
        "name":data.name,
        "lastname":data.lastname,
        "email":data.email,
        "password":hash.decode("utf-8")
    }
    existing_user = USER_DATA.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
 
    USER_DATA.insert_one(regester_data)

    return{"message":"User created successfully"}

# ----------------------------      LOG IN      --------------------------
class Login_data(BaseModel):
    email:EmailStr
    password:str
@app.post("/login")
async def login(data:Login_data ):
    user=USER_DATA.find_one({"email":data.email})
    
    if not user :
        raise HTTPException(status_code=400,detail="data not found")
    if not bcrypt.checkpw(data.password.encode("utf-8"),user["password"].encode("utf-8")):
        raise HTTPException(status_code=401 , detail="Invalid password")
    token_data = {
        "user_id":str(user["_id"]),
        "name":user["name"],
        "lastname":user["lastname"],
        "email":user["email"],
        "exp":datetime.utcnow() + timedelta(minutes=60)
    }
    token= jwt.encode(token_data,SECRET_KEY,algorithm="HS256")
    if not token:
        raise HTTPException(
            status_code=404,
            detail="data token not found"
        )
    return{"token":token}

# ----------------------------       PROFILE      --------------------------

@app.get("/profile")
async def profile(authorization:str = Header(None)):
    if not authorization :
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    parts  = authorization.split(" ")

    if len(parts ) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401)
    token=parts[1]
    try:
        decode= jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return {
    "user_id": decode["user_id"],
    "email": decode["email"]
}
    except JWTError:
        raise HTTPException(status_code=401,detail="data not found")