from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declared_attr

from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.adapters.mysql.models.exercise_plan_model import ExerciseTrainingModel
from workout_plan_server.adapters.mysql.models.generic_model import GenericModel
from workout_plan_server.domain.entities.training import Training


class TrainingModel(BaseModel, GenericModel):
    __tablename__ = "training"

    @declared_attr
    def workout_plan_id(self):
        return Column(String, ForeignKey("workout_plan.id"))

    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def exercises(self):
        return relationship("ExerciseTrainingModel", cascade="all, delete-orphan", lazy="select")

    @declared_attr
    def workout_plan(self):
        return relationship("WorkoutPlanModel", lazy="select")

    @staticmethod
    def from_entity(entity: Optional[Training]):
        if not entity:
            return None

        training_model = TrainingModel()
        training_model.fill_generic_entity(entity)
        training_model.workout_plan_id = entity.workout_plan.id
        training_model.start_date = entity.start_date
        training_model.end_date = entity.end_date
        training_model.exercises = [ExerciseTrainingModel.from_entity(exercise_plan, entity)
                                    for exercise_plan in entity.exercises]

        return training_model

    def to_entity(self):
        workout_plan = self.workout_plan.to_entity() if self.workout_plan_id else None
        exercises = [exercise.to_entity() for exercise in self.exercises]

        training = Training(workout_plan=workout_plan, exercises=exercises, start_date=self.start_date,
                            end_date=self.end_date)
        self.fill_generic_entity(training)

        return training
