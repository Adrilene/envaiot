from flask import Flask


app = Flask(__name__)


from .controller import configurator_controller
