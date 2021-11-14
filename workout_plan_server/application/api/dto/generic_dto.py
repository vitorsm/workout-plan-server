from flask_restx import fields

from workout_plan_server.application.api.dto.user_dto import user_dto


def generic_dto() -> dict:
    return {
        "id": fields.String(readOnly=True, description="Entity id"),
        "name": fields.String(required=True, description="Entity name"),
        "created_by": user_dto,
        "created_at": fields.DateTime(readOnly=True, description="When the entity was created"),
        "modified_by": user_dto,
        "modified_at": fields.DateTime(readOnly=True, description="Last time that entity was modified"),
    }
