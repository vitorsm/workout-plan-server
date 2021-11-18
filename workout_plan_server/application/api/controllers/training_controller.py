from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

from workout_plan_server.application.api.config.errors_handler import fill_error_handlers_to_controller
from workout_plan_server.application.api.mapper.training_mapper import TrainingMapper
from workout_plan_server.services.impl.training_service import TrainingService

training_controller = Blueprint("training_controller", __name__, url_prefix="/v1/training")
fill_error_handlers_to_controller(training_controller)


@training_controller.route("/", methods=["POST"])
@jwt_required()
def create_exercise(training_service: TrainingService):
    training = TrainingMapper.to_entity(request.json)
    training = training_service.create(training)
    return jsonify(TrainingMapper.to_dto(training)), 200


@training_controller.route("<path:training_id>", methods=["PUT"])
@jwt_required()
def update_workout_plan(training_id: str, training_service: TrainingService):
    training = TrainingMapper.to_entity(request.json)
    training.id = training_id

    training_service.update(training)
    return jsonify(TrainingMapper.to_dto(training)), 200


@training_controller.route("<path:training_id>", methods=["DELETE"])
@jwt_required()
def delete_training(training_id: str, training_service: TrainingService):
    training_service.delete(training_id)
    return "", 204


@training_controller.route("/", methods=["GET"])
@jwt_required()
def find_all_trainings(training_service: TrainingService):
    trainings = training_service.find_all_by_user()
    return jsonify([TrainingMapper.to_dto(training) for training in trainings]), 200


@training_controller.route("<path:training_id>", methods=["GET"])
@jwt_required()
def find_training_by_id(training_id: str, training_service: TrainingService):
    training = training_service.find_by_id(training_id)
    return jsonify(TrainingMapper.to_dto(training)), 200
