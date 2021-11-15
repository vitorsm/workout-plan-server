from flask_injector import FlaskInjector

from workout_plan_server import configs
from datetime import timedelta
from injector import Injector
from flask import Flask

from workout_plan_server.application.api.config.controllers_register import register_controllers
from workout_plan_server.application.api.config.dependencies_injector import DependenciesInjector


if not configs.TESTING:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
    app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)

    dependency_injector = Injector([DependenciesInjector(app)])

    register_controllers(app)
    FlaskInjector(app=app, injector=dependency_injector)

