# ------------------------------    IMPORT MODULES       ------------------------------------------#

from fastapi import APIRouter,HTTPException,Header
from schemas.user_schemas import Data ,Login_data
from utiles.securite import hash_password,verf_password,creat_token,decode_token
from database.conection import USER_DATA
from datetime import datetime,timedelta

# ------------------------------ server start  ------------------------------------------#

router=APIRouter()
@router.get("/")
async def root():
    return {"server":"start"}

# ------------------------------ REGISTER ENDPOINT  ------------------------------------------#

@router.post("/register")
async def register(data:Data):
    hashed= hash_password(data.password)
    regester_data={
        "name":data.name,
        "lastname":data.lastname,
        "email":data.email,
        "password":hashed
    }
    existing_user = USER_DATA.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
 
    USER_DATA.insert_one(regester_data)

    return{"message":"User created successfully"}

# ------------------------------ LOGIN ENDPOINT  ------------------------------------------#

@router.post("/login")
async def login(data:Login_data ):
    user=USER_DATA.find_one({"email":data.email})
    
    if not user :
        raise HTTPException(status_code=400,detail="data not found")
    if not verf_password(Login_data.password,user["password"]):
        raise HTTPException(status_code=401 , detail="Invalid password")
    token_data = {

    }
    token=creat_token({
            "user_id":str(user["_id"]),
            "name":user["name"],
            "lastname":user["lastname"],
            "email":user["email"],
            "exp":datetime.utcnow() + timedelta(minutes=60)})
    if not token:
        raise HTTPException(
            status_code=404,
            detail="data token not found"
        )
    return{"token":token}

# ------------------------------ PROFILE ENDPOINT  ------------------------------------------#

@router.get("/profile")
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
    decoded=decode_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token")