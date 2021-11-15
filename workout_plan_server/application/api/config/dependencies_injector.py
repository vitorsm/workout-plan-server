from flask import Flask
from injector import Module, Binder, singleton
from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.impl.mysql_exercise_repository import MySQLExerciseRepository
from workout_plan_server.adapters.mysql.impl.mysql_user_repository import MySQLUserRepository
from workout_plan_server.adapters.mysql.impl.mysql_workout_plan_repository import MySQLWorkoutPlanRepository
from workout_plan_server.application.api.flask_authentication_repository import FlaskAuthenticationRepository
from workout_plan_server.services.impl.exercise_service import ExerciseService
from workout_plan_server.services.impl.user_service import UserService
from workout_plan_server.services.impl.workout_plan_service import WorkoutPlanService
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository
from workout_plan_server.services.ports.user_repository import UserRepository
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class DependenciesInjector(Module):

    def __init__(self, app: Flask, db: SQLAlchemy = None):
        self.app = app
        self.db = db

    def configure(self, binder: Binder):
        if not self.db:
            self.db = SQLAlchemy(self.app, session_options={"autoflush": False})

        exercise_repository = MySQLExerciseRepository(self.db)
        user_repository = MySQLUserRepository(self.db)
        authentication_repository = FlaskAuthenticationRepository()
        workout_plan_repository = MySQLWorkoutPlanRepository(self.db)

        exercise_service = ExerciseService(authentication_repository, exercise_repository)
        user_service = UserService(user_repository, authentication_repository)
        workout_plan_service = WorkoutPlanService(workout_plan_repository, authentication_repository)

        # Repositories
        binder.bind(ExerciseRepository, to=exercise_repository, scope=singleton)
        binder.bind(UserRepository, to=user_repository, scope=singleton)
        binder.bind(WorkoutPlanRepository, to=workout_plan_repository, scope=singleton)

        # Services
        binder.bind(ExerciseService, to=exercise_service, scope=singleton)
        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(WorkoutPlanService, to=workout_plan_service, scope=singleton)
