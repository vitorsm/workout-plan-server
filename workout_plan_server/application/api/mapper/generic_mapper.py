from datetime import datetime
from typing import Optional

from workout_plan_server.application.api.mapper.user_mapper import UserMapper
from workout_plan_server.domain.entities.generic_entity import GenericEntity
from workout_plan_server.utils import date_utils


class GenericMapper(object):

    @staticmethod
    def fill_generic_entity(dto: Optional[dict], entity: GenericEntity):
        entity.id = dto.get("id")
        entity.name = dto.get("name")
        entity.created_at = date_utils.from_str_to_date(dto.get("created_at"))
        entity.modified_at = date_utils.from_str_to_date(dto.get("modified_at"))
        entity.created_by = UserMapper.to_entity(dto.get("created_by"))

    @staticmethod
    def fill_generic_dto(dto: Optional[dict], entity: GenericEntity):
        dto["id"] = entity.id
        dto["name"] = entity.name
        dto["created_at"] = entity.created_at.isoformat()
        dto["modified_at"] = entity.modified_at.isoformat()
        dto["created_by"] = UserMapper.to_dto(entity.created_by)
