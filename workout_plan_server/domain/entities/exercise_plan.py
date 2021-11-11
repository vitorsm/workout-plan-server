from dataclasses import dataclass
from typing import List

from workout_plan_server.domain.entities.exercise import Exercise


@dataclass
class ExerciseConfig(object):
    sets: int
    repetitions: int
    weight: float


@dataclass
class ExercisePlan(object):
    exercise: Exercise
    current_exercise_config: ExerciseConfig
    history_exercise_config: List[ExerciseConfig]
