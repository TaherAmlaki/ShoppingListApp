from dotenv import load_dotenv
from pathlib import Path 
import os 

# for testing without docker-compose, docker-compose does not need this
# webapp_env_path = "./env/webapp.env"
# load_dotenv(webapp_env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS")
JWT_AUTH_URL_RULE = os.getenv("JWT_AUTH_URL_RULE")
JWT_AUTH_USERNAME_KEY = os.getenv("JWT_AUTH_USERNAME_KEY")
MONGODB_SETTINGS = {"host": f"mongodb://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@mongodb:27017/ShoppingList?authSource=admin"}
