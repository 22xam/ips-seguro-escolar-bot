import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("IPS_USERNAME")
PASSWORD = os.getenv("IPS_PASSWORD")
