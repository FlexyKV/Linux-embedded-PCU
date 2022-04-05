from flask import Flask
from .config.config import get_login_password
from .web.api import record_controller, ports_controller, login_controller, config_controller

app = Flask(__name__)
app.register_blueprint(record_controller.bp)
app.register_blueprint(ports_controller.bp)
app.register_blueprint(login_controller.bp)
app.register_blueprint(config_controller.bp)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = get_login_password()
