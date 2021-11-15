from typing import Optional

from workout_plan_server.domain.entities.user import User


class UserMapper(object):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[User]:
        if not dto:
            return None

        return User(id=dto.get("id"), name=dto.get("name"), login=dto.get("login"), password=dto.get("password"))

    @staticmethod
    def to_dto(entity: Optional[User]) -> Optional[dict]:
        if not entity:
            return None

        return entity.__dict__
