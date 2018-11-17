import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DATABASE_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'alloua.db')
    THREAD_COUNT = 10
    BASE_URL = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?q='
    PROXY = dict({os.environ.get('PROXY').split(':')[0]: os.environ.get('PROXY')}) if os.environ.get('PROXY') else None
