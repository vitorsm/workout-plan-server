from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.exercise_model import ExerciseModel
from workout_plan_server.domain.entities.exercise import Exercise
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository


class MySQLExerciseRepository(GenericRepository[ExerciseModel], ExerciseRepository):

    def get_mapper(self):
        return

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, ExerciseModel)

    def merge_model_with_persisted_model(self, new_model: object) -> object:
        return None
