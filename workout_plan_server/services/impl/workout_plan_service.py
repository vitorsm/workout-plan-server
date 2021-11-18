from typing import List, Optional

from workout_plan_server.domain.entities.exercise import Exercise
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.generic_entity_service import GenericEntityService
from workout_plan_server.services.impl.exercise_service import ExerciseService
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository
from workout_plan_server.services.ports.workout_plan_repository import WorkoutPlanRepository


class WorkoutPlanService(GenericEntityService):

    def __init__(self, workout_plan_repository: WorkoutPlanRepository,
                 authentication_repository: AuthenticationRepository, exercise_service: ExerciseService):
        super().__init__(authentication_repository)
        self.workout_plan_repository = workout_plan_repository
        self.exercise_service = exercise_service

    def get_repository(self) -> WorkoutPlanRepository:
        return self.workout_plan_repository

    def get_entity_name(self) -> str:
        return "workout_plan"

    def prepare_to_persist(self, entity: WorkoutPlan):
        super().prepare_to_persist(entity)
        self.__fill_exercises(entity)

    def __fill_exercises(self, workout_plan: WorkoutPlan):
        exercise_ids = [exercise.exercise.id for exercise in workout_plan.exercises] if workout_plan.exercises else None

        if not exercise_ids:
            return

        exercises: List[Exercise] = self.exercise_service.find_all_by_ids(exercise_ids)
        exercise_plans = list()
        for exercise_plan in workout_plan.exercises:
            if not exercise_plan.exercise or not exercise_plan.exercise.id:
                continue

            exercise_plan.exercise = WorkoutPlanService.__find_exercise_by_id(exercises, exercise_plan.exercise.id)
            if exercise_plan.exercise:
                exercise_plans.append(exercise_plan)

        workout_plan.exercises = exercise_plans

    @staticmethod
    def __find_exercise_by_id(exercises: List[Exercise], exercise_id: str) -> Optional[Exercise]:
        return next((exercise for exercise in exercises if exercise.id == exercise_id), None)


