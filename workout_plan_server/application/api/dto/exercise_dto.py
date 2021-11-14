from flask_restx import fields

from workout_plan_server.application.api.dto.generic_dto import generic_dto

exercise_dto = generic_dto()
exercise_dto.update({
    "exercise_type": fields.String(required=True, description="Type of the exercise"),
    "body_type": fields.String(required=True, description="Body type of the exercise")
})
