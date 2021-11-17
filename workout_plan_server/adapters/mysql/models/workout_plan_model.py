from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship, declared_attr

from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.adapters.mysql.models.exercise_plan_model import ExercisePlanModel
from workout_plan_server.adapters.mysql.models.generic_model import GenericModel
from workout_plan_server.adapters.mysql.utils.model_utils import merge_lists
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan


class WorkoutPlanModel(BaseModel, GenericModel):
    __tablename__ = "workout_plan"
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def exercises(self):
        return relationship("ExercisePlanModel", cascade="all, delete-orphan", back_populates="workout_plan")

    @staticmethod
    def from_entity(entity: Optional[WorkoutPlan]):
        if not entity:
            return None

        model = WorkoutPlanModel()
        model.generic_from_entity(entity)

        model.start_date = entity.start_date
        model.end_date = entity.end_date
        model.exercises = [ExercisePlanModel.from_entity(exercise_plan, entity) for exercise_plan in entity.exercises]

        return model

    def to_entity(self, fetch_history: bool = True) -> WorkoutPlan:
        exercises_plan = [exercise_plan.to_entity(fetch_history) for exercise_plan in self.exercises]
        workout_plan = WorkoutPlan(exercises=exercises_plan, start_date=self.start_date, end_date=self.end_date)
        self.fill_generic_entity(workout_plan)

        return workout_plan

    def merge_model(self, workout_plan, models_to_add: list):
        """
        Will update this fields from workout_plan fields. If is necessary to add a new exercise, it will be added on
        models_to_add

        :param workout_plan: the workout_plan with the new fields
        :param models_to_add: list that will be updated with new exercise
        """

        super().merge_model(workout_plan, models_to_add)

        self.start_date = workout_plan.start_date
        self.end_date = workout_plan.end_date

        for exercise in workout_plan.exercises:
            exercise.workout_plan = self

        merge_lists(self.exercises, workout_plan.exercises, models_to_add)
