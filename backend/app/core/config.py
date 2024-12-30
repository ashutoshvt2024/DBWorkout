from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SANDBOX_DATABASE_URL = os.getenv("SANDBOX_DATABASE_URL")