from dataclasses import dataclass
from typing import List

from workout_plan_server.domain.entities.exercise_plan import ExercisePlan
from workout_plan_server.domain.entities.generic_entity import GenericEntity


@dataclass
class WorkoutPlan(GenericEntity):
    exercises: List[ExercisePlan]
