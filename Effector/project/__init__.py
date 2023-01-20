from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger
import os
app = Flask(__name__)
import logging

load_dotenv()
logging.basicConfig(
	filename=os.getenv("LOGS_PATH"),
	level=logging.INFO,
	format="%(asctime)s %(message)s"
)
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

from project import controller

