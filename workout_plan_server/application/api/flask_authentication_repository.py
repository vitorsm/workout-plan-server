from workout_plan_server.domain.entities.user import User
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository


class FlaskAuthenticationRepository(AuthenticationRepository):
    def get_current_user(self) -> User:
        return User(id="00000000-0000-0000-0000-000000000001", name="Admin", login="admin", password="admin")
