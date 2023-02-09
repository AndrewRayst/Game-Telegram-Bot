import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
API_KEY: str = os.getenv('API_KEY')
