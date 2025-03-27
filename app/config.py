import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde .env si estás en local

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
