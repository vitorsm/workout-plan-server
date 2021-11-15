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

    # def create(self, entity: Exercise) -> Exercise:
    #     exercise_model = ExerciseModel.from_entity(entity)
    #     exercise_model.id = str(uuid4())
    #
    #     self.add(exercise_model, commit=True)
    #
    #     return exercise_model.to_entity()
