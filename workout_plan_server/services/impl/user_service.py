from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.user_repository import UserRepository


class UserService(object):

    def __init__(self, user_repository: UserRepository, authentication_repository: AuthenticationRepository):
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository

    def create(self, user: User) -> User:
        user.id = None
        UserService.__assert_valid_user(user, True)

        return self.user_repository.create(user)

    def update(self, user: User):
        UserService.__assert_valid_user(user, False)
        current_user = self.get_current_user()

        if user != current_user:
            raise PermissionException("You don't have permission to modify this user")

        self.user_repository.update(user)

    def get_current_user(self) -> User:
        return self.authentication_repository.get_current_user()

    @staticmethod
    def __assert_valid_user(user: User, is_create: bool):
        missing_fields = user.get_missing_fields(is_create)

        if missing_fields:
            raise InvalidEntityException("user", missing_fields)
