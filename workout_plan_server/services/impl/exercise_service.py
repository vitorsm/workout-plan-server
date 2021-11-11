from workout_plan_server.services.generic_entity_service import GenericEntityService
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.entity_repository import EntityRepository
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository


class ExerciseService(GenericEntityService):

    def __init__(self, authentication_repository: AuthenticationRepository, exercise_repository: ExerciseRepository):
        super().__init__(authentication_repository)

        self.exercise_repository = exercise_repository

    def get_repository(self) -> EntityRepository:
        return self.exercise_repository

    def get_entity_name(self) -> str:
        return "exercise"

