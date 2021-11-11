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

    def get_missing_fields(self) -> List[str]:
        missing_fields = list()

        if not self.name:
            missing_fields.append("name")
        if not self.start_date:
            missing_fields.append("start_date")
        if not self.exercises:
            missing_fields.append("exercises")

        return missing_fields
