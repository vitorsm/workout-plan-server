from typing import Tuple, Optional

from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.workout_plan_model import WorkoutPlanModel
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class MySQLWorkoutPlanRepository(GenericRepository[WorkoutPlan], WorkoutPlanRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, WorkoutPlanModel)

    def merge_model_with_persisted_model(self, new_model: WorkoutPlanModel) -> Optional[Tuple[WorkoutPlanModel, list]]:
        persisted_model = self.find_model_by_id(new_model.id)
        models_to_add = list()
        persisted_model.merge_model(new_model, models_to_add)
        return persisted_model, models_to_add
