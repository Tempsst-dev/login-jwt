# ------------------------------    IMPORT MODULES       ------------------------------------------#

from pymongo import MongoClient
import os
from dotenv import load_dotenv
# ------------------------------    ENV       ------------------------------------------#

load_dotenv()
URL=os.getenv("URL")
# ------------------------------    DATA BASE CONECT       ------------------------------------------#

CLIENT=MongoClient(URL)
CREAT_USERS=CLIENT["CREAT_USERS"]
USER_DATA=CREAT_USERS["USER_DATA"]
