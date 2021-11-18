from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from workout_plan_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.encryption_adapter import EncryptionAdapter
from workout_plan_server.services.ports.user_repository import UserRepository


class UserService(object):

    def __init__(self, user_repository: UserRepository, authentication_repository: AuthenticationRepository,
                 encryption_adapter: EncryptionAdapter):
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository
        self.encryption_adapter = encryption_adapter

    def authenticate(self, login: str, password: str) -> User:
        user = self.user_repository.find_by_login(login)

        if not user or not self.encryption_adapter.check_encrypted_password(password, user.password):
            raise InvalidCredentialsException(login)

        return user

    def create(self, user: User) -> User:
        user.id = None
        UserService.__assert_valid_user(user, True)
        user.password = self.encryption_adapter.encrypt_password(user.password)

        return self.user_repository.create(user)

    def update(self, user: User):
        UserService.__assert_valid_user(user, False)
        current_user = self.get_current_user()

        if user != current_user:
            raise PermissionException("You don't have permission to modify this user")

        if user.password:
            user.password = self.encryption_adapter.encrypt_password(user.password)
        else:
            user.password = current_user.password

        self.user_repository.update(user)

    def get_current_user(self) -> User:
        return self.authentication_repository.get_current_user()

    @staticmethod
    def __assert_valid_user(user: User, is_create: bool):
        missing_fields = user.get_missing_fields(is_create)

        if missing_fields:
            raise InvalidEntityException("user", missing_fields)
