from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.workout_plan_model import WorkoutPlanModel
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class MySQLWorkoutPlanRepository(GenericRepository[WorkoutPlan], WorkoutPlanRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, WorkoutPlanModel)

    def merge_model_with_persisted_model(self, new_model: WorkoutPlanModel) -> WorkoutPlanModel:
        persisted_model = self.find_model_by_id(new_model.id)
        persisted_model.merge_model(new_model)
        return persisted_model
