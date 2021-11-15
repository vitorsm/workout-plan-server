from flask_jwt import current_identity

from workout_plan_server.domain.entities.user import User
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository


class FlaskAuthenticationRepository(AuthenticationRepository):
    def get_current_user(self) -> User:
        return current_identity
