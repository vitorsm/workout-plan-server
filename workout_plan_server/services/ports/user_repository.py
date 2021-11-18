import abc
from typing import Optional

from workout_plan_server.domain.entities.user import User


class UserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_login(self, login: str) -> Optional[User]:
        raise NotImplementedError
