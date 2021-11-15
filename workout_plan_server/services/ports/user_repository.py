import abc

from workout_plan_server.domain.entities.user import User


class UserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def authenticate(self, login: str, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError
