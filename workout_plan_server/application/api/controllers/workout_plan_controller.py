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


@workout_plan_controller.route("<path:workout_plan_id>", methods=["PUT"])
@jwt_required()
def update_workout_plan(workout_plan_id: str, workout_plan_service: WorkoutPlanService):
    workout_plan = WorkoutPlanMapper.to_entity(request.json)
    workout_plan.id = workout_plan_id

    workout_plan_service.update(workout_plan)
    return jsonify(WorkoutPlanMapper.to_dto(workout_plan)), 200


@workout_plan_controller.route("<path:workout_plan_id>", methods=["DELETE"])
@jwt_required()
def delete_workout_plan(workout_plan_id: str, workout_plan_service: WorkoutPlanService):
    workout_plan_service.delete(workout_plan_id)
    return "", 204


@workout_plan_controller.route("/", methods=["GET"])
@jwt_required()
def find_all_workout_plans(workout_plan_service: WorkoutPlanService):
    workout_plans = workout_plan_service.find_all_by_user()
    return jsonify([WorkoutPlanMapper.to_dto(workout_plan) for workout_plan in workout_plans]), 200


@workout_plan_controller.route("<path:workout_plan_id>", methods=["GET"])
@jwt_required()
def find_workout_plan_by_id(workout_plan_id: str, workout_plan_service: WorkoutPlanService):
    workout_plan = workout_plan_service.find_by_id(workout_plan_id)
    return jsonify(WorkoutPlanMapper.to_dto(workout_plan)), 200
