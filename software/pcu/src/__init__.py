from flask import Flask
from .web.api import record_controller, ports_controller

app = Flask(__name__)
app.register_blueprint(record_controller.bp)
app.register_blueprint(ports_controller.bp)

