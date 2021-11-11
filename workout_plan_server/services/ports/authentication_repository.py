import abc

from workout_plan_server.domain.entities.user import User


class AuthenticationRepository(metaclass=abc.ABCMeta):

    def get_current_user(self) -> User:
        """
        Get logged user
        """
        raise NotImplementedError
