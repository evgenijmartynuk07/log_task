import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get("SECRET")
DATABASE = os.environ.get("DATABASE")
DB_NAME = os.environ.get("DB_NAME")
AIO_DB = os.environ.get("AIO_DB")
