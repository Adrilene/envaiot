from flask import Flask
import os
from dotenv import load_dotenv
import logging

app = Flask(__name__)
load_dotenv()
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)

from project import controller