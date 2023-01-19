from flask import Flask
from dotenv import load_dotenv
import os
app = Flask(__name__)
import logging

load_dotenv()
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)

from project import controller

