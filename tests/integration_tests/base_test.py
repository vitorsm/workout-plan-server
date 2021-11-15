import os
from flask_testing import TestCase

from flask import Flask
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import Injector

from workout_plan_server import configs
from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.application.api import DependenciesInjector
from workout_plan_server.application.api.config import controllers_register
from workout_plan_server.utils import file_utils


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    app: Flask
    db: SQLAlchemy
    default_id: str

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = BaseTest.SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        configs.TESTING = True

        controllers_register.register_controllers(self.app)

        self.db = SQLAlchemy(self.app, session_options={"autoflush": False})

        dependency_injector = Injector([DependenciesInjector(self.app, self.db)])

        FlaskInjector(app=self.app, injector=dependency_injector)

        self.default_id = "00000000-0000-0000-0000-000000000001"
        self.secondary_default_id = "00000000-0000-0000-0000-000000000002"

        return self.app

    def setUp(self):
        BaseModel.metadata.create_all(self.db.get_engine())
        self.initial_load()
        self.db.session.commit()

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
