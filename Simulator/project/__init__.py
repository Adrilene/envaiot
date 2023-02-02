from flask import Flask
from flasgger import Swagger

template = {
  "swagger": "2.0",
  "info": {
    "title": "Simulator API",
    "description": "Swagger documentation of Enviot",
    "contact": {
      "responsibleOrganization": "GESAD",
      "responsibleDeveloper": "adrilene.fonseca@aluno.uece.br",
      "email": "adrilene.fonseca@aluno.uece.br",
      "url": "https://github.com/Adrilene",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
}


app = Flask(__name__)
swagger = Swagger(app, template=template)

from project import controller
