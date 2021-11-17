from typing import Optional

from workout_plan_server.application.api.mapper.exercise_mapper import ExerciseMapper
from workout_plan_server.domain.entities.exercise_plan import ExercisePlan, ExerciseConfig
from workout_plan_server.utils import date_utils


class ExercisePlanMapper(object):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[ExercisePlan]:
        if not dto:
            return None

        exercise = ExerciseMapper.to_entity(dto.get("exercise"))
        current_exercise_config = ExercisePlanMapper.__exercise_config_to_entity(dto.get("current_exercise_config"))
        history_exercise_config = [ExercisePlanMapper.__exercise_config_to_entity(hec)
                                   for hec in dto.get("history_exercise_config")] \
            if dto.get("history_exercise_config") else None

        return ExercisePlan(exercise=exercise, current_exercise_config=current_exercise_config,
                            history_exercise_config=history_exercise_config)

    @staticmethod
    def to_dto(exercise_plan: Optional[ExercisePlan]) -> Optional[dict]:
        if not exercise_plan:
            return None

        exercise_config = ExercisePlanMapper.__exercise_config_to_dict(exercise_plan.current_exercise_config)
        history_exercise_config = [ExercisePlanMapper.__exercise_config_to_dict(hec)
                                   for hec in exercise_plan.history_exercise_config] \
            if exercise_plan.history_exercise_config else None

        return {
            "exercise": ExerciseMapper.to_dto(exercise_plan.exercise),
            "current_exercise_config": exercise_config,
            "history_exercise_config": history_exercise_config
        }

    @staticmethod
    def __exercise_config_to_entity(dto: Optional[dict]) -> Optional[ExerciseConfig]:
        if not dto:
            return None

        return ExerciseConfig(sets=dto.get("sets"), repetitions=dto.get("repetitions"),
                              weight=dto.get("weight"),
                              start_date=date_utils.from_str_to_date(dto.get("start_date")))

    @staticmethod
    def __exercise_config_to_dict(exercise_config: ExerciseConfig) -> Optional[dict]:
        if not exercise_config:
            return None

        return {
            "sets": exercise_config.sets,
            "repetitions": exercise_config.repetitions,
            "weight": exercise_config.weight,
            "start_date": exercise_config.start_date.isoformat() if exercise_config.start_date else None
        }
