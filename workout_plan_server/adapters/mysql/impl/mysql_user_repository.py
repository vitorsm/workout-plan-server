from typing import Optional

from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.user_model import UserModel
from workout_plan_server.domain.entities.user import User
from workout_plan_server.services.ports.user_repository import UserRepository


class MySQLUserRepository(GenericRepository[UserModel], UserRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, UserModel)

    def find_by_login(self, login: str) -> Optional[User]:
        model = self.db.session.query(self.entity_type).filter(UserModel.login == login).first()

        if not model:
            return None

        return model.to_entity()

    def merge_model_with_persisted_model(self, new_model: object) -> object:
        return None
