import os
from datetime import timedelta

from flask_testing import TestCase

from flask import Flask
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import Injector

from workout_plan_server import configs
from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.application.api import DependenciesInjector, fill_jwt_auth_functions
from workout_plan_server.application.api.config import controllers_register
from workout_plan_server.domain.entities.user import User
from workout_plan_server.utils import file_utils


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    app: Flask
    db: SQLAlchemy
    default_id: str
    token: str

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = BaseTest.SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
        self.app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
        self.app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)

        controllers_register.register_controllers(self.app)

        self.db = SQLAlchemy(self.app, session_options={"autoflush": False})
        dependency_injector = Injector([DependenciesInjector(self.app, self.db)])
        FlaskInjector(app=self.app, injector=dependency_injector)
        self.jwt = fill_jwt_auth_functions(self.app, dependency_injector)

        self.default_id = "00000000-0000-0000-0000-000000000001"
        self.secondary_default_id = "00000000-0000-0000-0000-000000000002"

        return self.app

    def setUp(self):
        BaseModel.metadata.create_all(self.db.get_engine())
        self.initial_load()
        self.db.session.commit()

        default_user = self.__get_default_user()
        self.token = "JWT " + self.jwt.jwt_encode_callback(default_user).decode()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def initial_load(self):
        file_path = os.path.join(file_utils.get_project_dir(), "resources", "db", "initial_load.sql")
        file = open(file_path, "r")
        for query in file.read().split(";"):
            if query.strip():
                self.db.session.execute(query.strip())
        file.close()

    def __get_default_user(self) -> User:
        return User(id=self.default_id, name="Admin", login="admin", password="admin")

    def get_authentication_header(self) -> dict:
        return {
            "Authorization": self.token
        }
