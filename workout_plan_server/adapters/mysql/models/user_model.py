from typing import Optional

from sqlalchemy import Column, String

from workout_plan_server.adapters.mysql.models import BaseModel
from workout_plan_server.domain.entities.user import User


class UserModel(BaseModel):
    __tablename__ = "user"
    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def from_entity(entity: Optional[User]):
        if not entity:
            return None

        user = UserModel()
        user.id = entity.id
        user.name = entity.name
        user.login = entity.login
        user.password = entity.password
        return user

    def to_entity(self) -> User:
        return User(id=self.id, name=self.name, login=self.login, password=self.password)
