from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

from workout_plan_server.application.api.config.errors_handler import fill_error_handlers_to_controller
from workout_plan_server.application.api.mapper.workout_plan_mapper import WorkoutPlanMapper
from workout_plan_server.services.impl.workout_plan_service import WorkoutPlanService

workout_plan_controller = Blueprint("workout_plan_controller", __name__, url_prefix="/v1/workout-plan")
fill_error_handlers_to_controller(workout_plan_controller)


@workout_plan_controller.route("/", methods=["POST"])
@jwt_required()
def create_exercise(workout_plan_service: WorkoutPlanService):
    workout_plan = WorkoutPlanMapper.to_entity(request.json)
    workout_plan = workout_plan_service.create(workout_plan)
    return jsonify(WorkoutPlanMapper.to_dto(workout_plan)), 200
