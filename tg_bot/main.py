from requests import get, post
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()  # автоматически ищет .env в корне проекта
print(find_dotenv())  # посмотри, есть ли переменные в окружении

print(os.getenv("CLIENT_SECRET"))
print(os.getenv("CLIENT_ID"))