from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from workout_plan_server.adapters.mysql.models.exercise_model import ExerciseModel
from workout_plan_server.adapters.mysql.models.exercise_plan_model import ExercisePlanModel, HistoryExercisePlanModel, \
    ExerciseTrainingModel
from workout_plan_server.adapters.mysql.models.training_model import TrainingModel
from workout_plan_server.adapters.mysql.models.user_model import UserModel
from workout_plan_server.adapters.mysql.models.workout_plan_model import WorkoutPlanModel

