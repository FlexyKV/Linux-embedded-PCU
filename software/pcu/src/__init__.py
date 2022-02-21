from flask import Flask
from .api import pcu_controller

app = Flask(__name__)
app.register_blueprint(pcu_controller.bp)
