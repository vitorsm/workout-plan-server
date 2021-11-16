from flask_sqlalchemy import SQLAlchemy

from workout_plan_server.adapters.mysql.generic_repository import GenericRepository
from workout_plan_server.adapters.mysql.models.user_model import UserModel
from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from workout_plan_server.services.ports.user_repository import UserRepository


class MySQLUserRepository(GenericRepository[UserModel], UserRepository):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, UserModel)

    def authenticate(self, login: str, password: str) -> User:
        user = self.db.session.query(UserModel)\
            .filter(UserModel.login == login and UserModel.password == password).first()

        if not user:
            raise InvalidCredentialsException(login)

        return user.to_entity()

    def merge_model_with_persisted_model(self, new_model: object) -> object:
        return None
