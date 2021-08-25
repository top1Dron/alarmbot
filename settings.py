from configparser import ConfigParser


#instantiate
config = ConfigParser()

#parse config.ini file
config.read('config.ini')

#read values from config.ini
ADMINS = config.get('bot_section', 'ADMINS').split(',')
admin_id = [int(id) for id in ADMINS]
TOKEN = config.get('bot_section', 'BOT_TOKEN')
ip = config.get('bot_section', 'ip')

user = config.get('db_section', 'POSTGRES_USER')
password = config.get('db_section', 'POSTGRES_PASSWORD')
db_name = config.get('db_section', 'POSTGRES_DB')
host = config.get('db_section', 'POSTGRES_HOST')
port = config.get('db_section', 'POSTGRES_PORT')
db_url = f'postgres://{user}:{password}@{host}:{port}/{db_name}'

CELERY_BROKER_URL = config.get('celery_section', 'CELERY_BROKER')
CELERY_RESULT_BACKEND = config.get('celery_section', 'CELERY_BACKEND')