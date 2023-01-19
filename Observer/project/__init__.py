from flask import Flask
import os
from dotenv import load_dotenv

app = Flask(__name__)
import logging
load_dotenv
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)

from project import controller
