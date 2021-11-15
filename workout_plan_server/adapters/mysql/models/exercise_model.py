from typing import Optional

from sqlalchemy import Column, String

from workout_plan_server.adapters.mysql.models.generic_model import GenericModel
from workout_plan_server.domain.entities.exercise import Exercise


class ExerciseModel(GenericModel):
    __tablename__ = "exercise"
    exercise_type = Column(String, nullable=False)
    body_type = Column(String, nullable=False)

    @staticmethod
    def from_entity(entity: Optional[Exercise]):
        if not entity:
            return None

        exercise_model = ExerciseModel()
        exercise_model.generic_from_entity(entity)
        exercise_model.exercise_type = entity.exercise_type.name
        exercise_model.body_type = entity.body_type.name

    def to_entity(self, fetch_created_by: bool = True) -> Exercise:
        exercise = Exercise(Exercise.instantiate_exercise_type_by_name(self.exercise_type),
                            body_type=Exercise.instantiate_body_type_by_name(self.body_type))
        self.fill_generic_entity(exercise, fetch_created_by)
        return exercise
