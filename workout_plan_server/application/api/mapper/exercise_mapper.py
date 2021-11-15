from typing import Optional

from workout_plan_server.application.api.mapper.generic_mapper import GenericMapper
from workout_plan_server.domain.entities.exercise import Exercise


class ExerciseMapper(object):
    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Exercise]:
        if not dto:
            return None

        exercise = Exercise(exercise_type=Exercise.instantiate_exercise_type_by_name(dto.get("exercise_type")),
                            body_type=Exercise.instantiate_body_type_by_name(dto.get("body_type")))

        GenericMapper.fill_generic_entity(dto, exercise)

        return exercise

    @staticmethod
    def to_dto(entity: Optional[Exercise]) -> Optional[dict]:
        if not entity:
            return None

        dto = {
            "exercise_type": entity.exercise_type.name,
            "body_type": entity.body_type.name
        }

        GenericMapper.fill_generic_dto(dto, entity)

        return dto
