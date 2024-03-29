from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship, declared_attr

from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.adapters.mysql.utils.model_utils import merge_lists
from workout_plan_server.domain.entities.exercise import Exercise
from workout_plan_server.domain.entities.exercise_plan import ExercisePlan, ExerciseConfig
from workout_plan_server.domain.entities.training import Training
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan


class ExercisePlanModel(BaseModel):
    __tablename__ = "exercise_plan"

    sets = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def exercise_id(self):
        return Column(String, ForeignKey("exercise.id"), nullable=False, primary_key=True)

    @declared_attr
    def workout_plan_id(self):
        return Column(String, ForeignKey("workout_plan.id"), nullable=False, primary_key=True)

    @declared_attr
    def workout_plan(self):
        return relationship("WorkoutPlanModel", lazy="select")

    @declared_attr
    def history_exercise_config(self):
        return relationship("HistoryExercisePlanModel", cascade="all, delete-orphan", lazy="select")

    @declared_attr
    def exercise(self):
        return relationship("ExerciseModel", lazy="select")

    def __eq__(self, other):
        return other and self.exercise_id == other.exercise_id and self.workout_plan_id == other.workout_plan_id

    @staticmethod
    def from_entity(entity: Optional[ExercisePlan], workout_plan: WorkoutPlan):
        if not entity:
            return None

        exercise_plan_model = ExercisePlanModel()
        exercise_plan_model.exercise_id = entity.exercise.id
        exercise_plan_model.workout_plan_id = workout_plan.id
        exercise_plan_model.sets = entity.current_exercise_config.sets
        exercise_plan_model.repetitions = entity.current_exercise_config.repetitions
        exercise_plan_model.weight = entity.current_exercise_config.weight

        exercise_plan_model.history_exercise_config = \
            [HistoryExercisePlanModel.instantiate(exercise_config, entity.exercise, workout_plan)
             for exercise_config in entity.history_exercise_config] if entity.history_exercise_config else list()

        return exercise_plan_model

    def to_entity(self, fetch_history: bool = True) -> ExercisePlan:
        exercise_config = ExerciseConfig(sets=self.sets, repetitions=self.repetitions, weight=self.weight,
                                         start_date=self.start_date)

        history_exercise_config = list()

        if fetch_history:
            history_exercise_config = [ExerciseConfig(sets=hec.sets, repetitions=hec.repetitions, weight=hec.weight,
                                                      start_date=hec.start_date) for hec in self.history_exercise_config]

        return ExercisePlan(exercise=self.exercise.to_entity(), current_exercise_config=exercise_config,
                            history_exercise_config=history_exercise_config)

    def merge_model(self, exercise_plan, models_to_add: list):
        """
        Will update this fields from exercise_plan fields. If is necessary to add a new history_exercise_config,
        it will be added on models_to_add

        :param exercise_plan: the exercise_plan with the new fields
        :param models_to_add: list that will be updated with new history_exercise_config
        """

        self.sets = exercise_plan.sets
        self.repetitions = exercise_plan.repetitions
        self.weight = exercise_plan.weight
        self.exercise_id = exercise_plan.exercise_id

        if exercise_plan.start_date:
            self.start_date = exercise_plan.start_date

        merge_lists(self.history_exercise_config, exercise_plan.history_exercise_config, models_to_add)


class HistoryExercisePlanModel(BaseModel):
    __tablename__ = "history_exercise_plan"

    start_date = Column(DateTime, nullable=False, default=datetime.utcnow, primary_key=True)
    sets = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    @declared_attr
    def exercise_id(self):
        return Column(String, nullable=False, primary_key=True)

    @declared_attr
    def workout_plan_id(self):
        return Column(String, nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(["workout_plan_id", "exercise_id"],
                                           [ExercisePlanModel.workout_plan_id, ExercisePlanModel.exercise_id]), {})

    def __eq__(self, other):
        return other and self.exercise_id == other.exercise_id and self.workout_plan_id == other.workout_plan_id \
               and self.start_date == other.start_date

    @staticmethod
    def instantiate(exercise_config: ExerciseConfig, exercise: Exercise, workout_plan: WorkoutPlan):
        history_exercise = HistoryExercisePlanModel()
        history_exercise.exercise_id = exercise.id
        history_exercise.workout_plan_id = workout_plan.id
        history_exercise.start_date = exercise_config.start_date
        history_exercise.sets = exercise_config.sets
        history_exercise.repetitions = exercise_config.repetitions
        history_exercise.weight = exercise_config.weight

        return history_exercise

    def merge_model(self, history, models_to_add: list):
        """
        Will update this fields from history fields. The models_to_add will be ignored, it is only for the contract

        :param history: the exercise_plan with the new fields
        :param models_to_add: list that will be ignored
        """

        self.start_date = history.start_date
        self.sets = history.sets
        self.repetitions = history.repetitions
        self.weight = history.weight


class ExerciseTrainingModel(BaseModel):
    __tablename__ = "exercise_training"

    @declared_attr
    def exercise_id(self):
        return Column(String, ForeignKey("exercise.id"), nullable=False, primary_key=True)

    @declared_attr
    def training_id(self):
        return Column(String, ForeignKey("training.id"), nullable=False, primary_key=True)

    @declared_attr
    def training(self):
        return relationship("TrainingModel", lazy="select")

    sets = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    @declared_attr
    def exercise(self):
        return relationship("ExerciseModel", lazy="select")

    def __eq__(self, other):
        return other and self.exercise_id == other.exercise_id and self.training_id == other.training_id

    @staticmethod
    def from_entity(entity: Optional[ExercisePlan], training: Training):
        if not entity:
            return None

        exercise_training_model = ExerciseTrainingModel()
        exercise_training_model.exercise_id = entity.exercise.id
        exercise_training_model.training_id = training.id
        exercise_training_model.sets = entity.current_exercise_config.sets
        exercise_training_model.repetitions = entity.current_exercise_config.repetitions
        exercise_training_model.weight = entity.current_exercise_config.weight

        return exercise_training_model

    def to_entity(self) -> ExercisePlan:
        exercise_config = ExerciseConfig(sets=self.sets, repetitions=self.repetitions, weight=self.weight,
                                         start_date=None)
        return ExercisePlan(exercise=self.exercise.to_entity(), current_exercise_config=exercise_config,
                            history_exercise_config=list())

    def merge_model(self, exercise_training, models_to_add: list):
        """
        Will update this fields from exercise_training fields. The models_to_add will be ignored, it is only
        for the contract

        :param exercise_training: the exercise_training with the new fields
        :param models_to_add: list that will be ignored
        """
        self.sets = exercise_training.sets
        self.repetitions = exercise_training.repetitions
        self.weight = exercise_training.weight
