import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_TOKEN = os.getenv("SECRET_TOKEN", "admin_secret")
    # Spin up a local redis server
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    WEBSITE_URL = os.getenv("WEBSITE_URL", "https://dentalstall.com/shop/")