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
