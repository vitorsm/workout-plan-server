from typing import Optional

from workout_plan_server.application.api.mapper.exercise_plan_mapper import ExercisePlanMapper
from workout_plan_server.application.api.mapper.generic_mapper import GenericMapper
from workout_plan_server.application.api.mapper.workout_plan_mapper import WorkoutPlanMapper
from workout_plan_server.domain.entities.training import Training
from workout_plan_server.utils import date_utils


class TrainingMapper(object):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Training]:
        if not dto:
            return None

        exercises = [ExercisePlanMapper.to_entity(exercise_dto) for exercise_dto in dto.get("exercises")] \
            if dto.get("exercises") else None

        workout_plan = WorkoutPlanMapper.to_entity(dto.get("workout_plan"))
        start_date = date_utils.from_str_to_date(dto.get("start_date"))
        end_date = date_utils.from_str_to_date(dto.get("end_date"))

        training = Training(workout_plan=workout_plan, exercises=exercises, start_date=start_date,
                            end_date=end_date, name=dto.get("name"), training_id=dto.get("id"))
        GenericMapper.fill_generic_entity(dto, training)

        return training

    @staticmethod
    def to_dto(training: Optional[Training]) -> Optional[dict]:
        if not training:
            return None

        exercises = [ExercisePlanMapper.to_dto(exercise) for exercise in training.exercises] \
            if training.exercises else training.exercises

        dto = {
            "start_date": training.start_date.isoformat(),
            "end_date": training.end_date.isoformat() if training.end_date else None,
            "workout_plan": WorkoutPlanMapper.to_dto(training.workout_plan),
            "exercises": exercises
        }

        GenericMapper.fill_generic_dto(dto, training)

        return dto
