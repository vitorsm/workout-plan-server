import enum
from dataclasses import dataclass

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
