from flask import Flask
from .web.api import record_controller, ports_controller, login_controller
from .web.api.login_validation.login_validation import key


app = Flask(__name__)
app.register_blueprint(record_controller.bp)
app.register_blueprint(ports_controller.bp)
app.register_blueprint(login_controller.bp)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = key
