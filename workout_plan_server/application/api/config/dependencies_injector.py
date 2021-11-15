from flask import Flask
from injector import Module, Binder, singleton
from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.impl.mysql_exercise_repository import MySQLExerciseRepository
from workout_plan_server.application.api.flask_authentication_repository import FlaskAuthenticationRepository
from workout_plan_server.services.impl.exercise_service import ExerciseService
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository


class DependenciesInjector(Module):

    def __init__(self, app: Flask, db: SQLAlchemy = None):
        self.app = app
        self.db = db

    def configure(self, binder: Binder):
        if not self.db:
            self.db = SQLAlchemy(self.app, session_options={"autoflush": False})

        exercise_repository = MySQLExerciseRepository(self.db)

        authentication_repository = FlaskAuthenticationRepository()

        exercise_service = ExerciseService(authentication_repository, exercise_repository)

        # Repositories
        binder.bind(ExerciseRepository, to=exercise_repository, scope=singleton)

        # Services
        binder.bind(ExerciseService, to=exercise_service, scope=singleton)
