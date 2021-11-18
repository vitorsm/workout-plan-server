from typing import Optional, Tuple

from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models import TrainingModel
from workout_plan_server.domain.entities.training import Training
from workout_plan_server.services.ports.training_repository import TrainingRepository


class MySQLTrainingRepository(GenericRepository[Training], TrainingRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, TrainingModel)

    def merge_model_with_persisted_model(self, new_model: object) -> Optional[Tuple[TrainingModel, list]]:
        persisted_model = self.find_model_by_id(new_model.id)
        models_to_add = list()
        persisted_model.merge_model(new_model, models_to_add)

        return persisted_model, models_to_add
