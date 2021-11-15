from workout_plan_server.services.generic_entity_service import GenericEntityService
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class WorkoutPlanService(GenericEntityService):

    def __init__(self, workout_plan_repository: WorkoutPlanRepository,
                 authentication_repository: AuthenticationRepository):
        super().__init__(authentication_repository)
        self.workout_plan_repository = workout_plan_repository

    def get_repository(self) -> WorkoutPlanRepository:
        return self.workout_plan_repository

    def get_entity_name(self) -> str:
        return "workout_plan"
