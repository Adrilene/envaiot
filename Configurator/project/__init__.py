import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)

template = {
	"swagger": "2.0",
	"info":{
		"title": "EnvAIoT API",
		"description": "API for validating adaptation strategies in IoT systems.",
		"contact": {
			"responsibleOrganization": "GESAD",
			"responsibleDeveloper": "Adrilene Fonseca",
			"email": "adrilene.fonseca@aluno.uece.br"
		},
		"version": "0.0.1"
	}
}

swagger = Swagger(app, template=template)

load_dotenv()
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)

from project import controller
