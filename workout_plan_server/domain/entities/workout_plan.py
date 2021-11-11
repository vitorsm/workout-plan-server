from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from workout_plan_server.domain.entities.exercise_plan import ExercisePlan
from workout_plan_server.domain.entities.generic_entity import GenericEntity


@dataclass
class WorkoutPlan(GenericEntity):
    exercises: List[ExercisePlan]
    start_date: datetime
    end_date: Optional[datetime]
