from typing import List, Optional

from workout_plan_server.domain.entities.exercise import Exercise
from workout_plan_server.domain.entities.training import Training
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.generic_entity_service import GenericEntityService
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.entity_repository import EntityRepository
from workout_plan_server.services.ports.exercise_repository import ExerciseRepository
from workout_plan_server.services.ports.training_repository import TrainingRepository


class TrainingService(GenericEntityService):

    def __init__(self, authentication_repository: AuthenticationRepository, training_repository: TrainingRepository,
                 exercise_repository: ExerciseRepository):
        super().__init__(authentication_repository)

        self.training_repository = training_repository
        self.exercise_repository = exercise_repository

    def get_repository(self) -> EntityRepository:
        return self.training_repository

    def get_entity_name(self) -> str:
        return "training"

    def prepare_to_persist(self, entity: Training):
        if not entity:
            return

        super().prepare_to_persist(entity)
        self.__fill_exercises(entity)

    def valid_to_persist(self, entity: Training, to_delete: bool):
        super().valid_to_persist(entity, to_delete)

        if to_delete:
            return

        if not entity.exercises:
            return

        user = self.authentication_repository.get_current_user()

        for exercise_plan in entity.exercises:
            if exercise_plan.exercise.created_by != user:
                raise PermissionException("You don't have permission to use exercise from other users")

    def __fill_exercises(self, training: Training):
        exercise_ids = [exercise.exercise.id for exercise in training.exercises] if training.exercises else None

        if not exercise_ids:
            return

        exercises: List[Exercise] = self.exercise_repository.find_all_by_ids(exercise_ids)
        exercise_plans = list()
        for exercise_plan in training.exercises:
            if not exercise_plan.exercise or not exercise_plan.exercise.id:
                continue

            exercise_plan.exercise = TrainingService.__find_exercise_by_id(exercises, exercise_plan.exercise.id)
            if exercise_plan.exercise:
                exercise_plans.append(exercise_plan)

        training.exercises = exercise_plans

    @staticmethod
    def __find_exercise_by_id(exercises: List[Exercise], exercise_id: str) -> Optional[Exercise]:
        return next((exercise for exercise in exercises if exercise.id == exercise_id), None)
