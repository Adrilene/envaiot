from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
load_dotenv()

from project import controller
