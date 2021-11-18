from typing import Optional

from workout_plan_server.application.api.mapper.exercise_plan_mapper import ExercisePlanMapper
from workout_plan_server.application.api.mapper.generic_mapper import GenericMapper
from workout_plan_server.domain.entities.workout_plan import WorkoutPlan
from workout_plan_server.utils import date_utils


class WorkoutPlanMapper(object):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[WorkoutPlan]:
        if not dto:
            return None

        exercises = [ExercisePlanMapper.to_entity(exercise_dto) for exercise_dto in dto.get("exercises")] \
            if dto.get("exercises") else None

        workout_plan = WorkoutPlan(exercises=exercises, start_date=date_utils.from_str_to_date(dto.get("start_date")),
                                   end_date=date_utils.from_str_to_date(dto.get("end_date")))

        GenericMapper.fill_generic_entity(dto, workout_plan)

        return workout_plan

    @staticmethod
    def to_dto(workout_plan: Optional[WorkoutPlan]) -> Optional[dict]:
        if not workout_plan:
            return None

        exercises = [ExercisePlanMapper.to_dto(exercise) for exercise in workout_plan.exercises] \
            if workout_plan.exercises else None

        dto = {
            "exercises": exercises,
            "start_date": workout_plan.start_date.isoformat() if workout_plan.start_date else None,
            "end_date": workout_plan.end_date.isoformat() if workout_plan.end_date else None
        }

        GenericMapper.fill_generic_dto(dto, workout_plan)

        return dto
