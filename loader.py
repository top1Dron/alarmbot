import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from google_settings import create_service
import settings


bot = Bot(token=settings.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
working_dir = os.getcwd()
token_dir = 'token files'
CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_SERVICE_FILE = 'service_client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
USER_EMAIL = 'andrew.moshko'
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def create_google_service():
    global service
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)