from flask import Flask
import os
from dotenv import load_dotenv
import logging

load_dotenv()
print(os.getenv('CONFIGURATOR_HOST'),flush=True)
print(os.getenv('SIMULATOR_HOST'),flush=True)
print(os.getenv('OBSERVER_HOST'),flush=True)
print(os.getenv('EFFECTOR_HOST'),flush=True)
app = Flask(__name__)
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)

from project import controller