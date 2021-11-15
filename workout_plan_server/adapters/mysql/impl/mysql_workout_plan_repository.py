from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.workout_plan_model import WorkoutPlanModel
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class MySQLWorkoutPlanRepository(GenericRepository[WorkoutPlanModel], WorkoutPlanRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, WorkoutPlanModel)
