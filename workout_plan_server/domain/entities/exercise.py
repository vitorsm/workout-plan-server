import enum
from dataclasses import dataclass
from typing import List

from workout_plan_server.domain.entities.generic_entity import GenericEntity


class ExerciseType(enum.Enum):
    CARDIO = 1
    MUSCLE = 2


class ExerciseBodyType(enum.Enum):
    UPPER = 1
    LOWER = 2


@dataclass
class Exercise(GenericEntity):
    exercise_type: ExerciseType
    body_type: ExerciseBodyType

    def get_missing_fields(self) -> List[str]:
        missing_fields = list()

        if not self.name:
            missing_fields.append("name")
        if not self.exercise_type:
            missing_fields.append("exercise_type")
        if not self.body_type:
            missing_fields.append("body_type")

        return missing_fields

    @staticmethod
    def instantiate_exercise_type_by_name(exercise_type_name: str) -> ExerciseType:
        exercise_types = list(map(lambda t: t, ExerciseType))
        return next((t for t in exercise_types if t.name == exercise_type_name), None)

    @staticmethod
    def instantiate_body_type_by_name(body_type_name: str) -> ExerciseBodyType:
        body_types = list(map(lambda t: t, ExerciseBodyType))
        return next((t for t in body_types if t.name == body_type_name), None)
