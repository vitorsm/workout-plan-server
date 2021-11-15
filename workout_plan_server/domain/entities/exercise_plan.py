from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from workout_plan_server.domain.entities.exercise import Exercise


@dataclass
class ExerciseConfig(object):
    sets: int
    repetitions: int
    weight: float
    start_date: Optional[datetime]


@dataclass
class ExercisePlan(object):
    exercise: Exercise
    current_exercise_config: ExerciseConfig
    history_exercise_config: List[ExerciseConfig]
