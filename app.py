from os import getenv
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True} 
app.secret_key = getenv('SECRET_KEY')
import routes