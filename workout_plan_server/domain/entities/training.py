from datetime import datetime
from typing import Optional, List

from workout_plan_server.domain.entities.exercise_plan import ExercisePlan
from workout_plan_server.domain.entities.generic_entity import GenericEntity
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan


class Training(GenericEntity):
    workout_plan: Optional[WorkoutPlan]
    exercises: List[ExercisePlan]
    start_date: datetime
    end_date: Optional[datetime]

    def __init__(self, workout_plan: Optional[WorkoutPlan], exercises: List[ExercisePlan], start_date: datetime,
                 end_date: Optional[datetime], name: Optional[str] = None, training_id: Optional[str] = None):
        self.workout_plan = workout_plan
        self.exercises = exercises
        self.start_date = start_date
        self.end_date = end_date
        self.name = name if name else self.__generate_training_name()
        self.id = training_id

    def __generate_training_name(self) -> str:
        return f"Training {self.start_date.date()}"
