from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from workout_plan_server.adapters.mysql.models.training_model import TrainingModel
