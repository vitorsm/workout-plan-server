from flask import Blueprint, request, jsonify

from workout_plan_server.application.api.config.errors_handler import fill_error_handlers_to_controller
from workout_plan_server.application.api.mapper.exercise_mapper import ExerciseMapper
from workout_plan_server.services.impl.exercise_service import ExerciseService

exercise_controller = Blueprint("exercise_controller", __name__, url_prefix="/v1/exercise")
fill_error_handlers_to_controller(exercise_controller)


@exercise_controller.route("/", methods=["POST"])
def create_exercise(exercise_service: ExerciseService):
    exercise = ExerciseMapper.to_entity(request.json)
    exercise = exercise_service.create(exercise)
    return jsonify(ExerciseMapper.to_dto(exercise)), 200


@exercise_controller.route("<path:exercise_id>", methods=["PUT"])
def update_exercise(exercise_id: str, exercise_service: ExerciseService):
    exercise = ExerciseMapper.to_entity(request.json)
    exercise.id = exercise_id

    exercise_service.update(exercise)
    return jsonify(ExerciseMapper.to_dto(exercise)), 200


@exercise_controller.route("<path:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id: str, exercise_service: ExerciseService):
    exercise_service.delete(exercise_id)
    return "", 204


@exercise_controller.route("<path:exercise_id>", methods=["GET"])
def find_exercise_by_id(exercise_id: str, exercise_service: ExerciseService):
    exercise = exercise_service.find_by_id(exercise_id)
    return jsonify(ExerciseMapper.to_dto(exercise)), 200


@exercise_controller.route("/", methods=["GET"])
def find_all_exercises(exercise_service: ExerciseService):
    exercises = exercise_service.find_all_by_user()
    return jsonify([ExerciseMapper.to_dto(exercise) for exercise in exercises]), 200

