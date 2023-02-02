from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
load_dotenv()

from project import controller
