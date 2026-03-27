# ------------------------------    IMPORT MODULES       ------------------------------------------#

from fastapi import FastAPI ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router


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
app.include_router(router)


