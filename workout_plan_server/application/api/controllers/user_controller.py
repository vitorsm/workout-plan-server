from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

from workout_plan_server.application.api.config.errors_handler import fill_error_handlers_to_controller
from workout_plan_server.application.api.mapper.user_mapper import UserMapper
from workout_plan_server.services.impl.user_service import UserService

user_controller = Blueprint("user_controller", __name__, url_prefix="/v1/user")
fill_error_handlers_to_controller(user_controller)


@user_controller.route("/", methods=["POST"])
def create_user(user_service: UserService):
    user = UserMapper.to_entity(request.json)
    user = user_service.create(user)
    return jsonify(UserMapper.to_dto(user)), 200


@user_controller.route("<path:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id: str, user_service: UserService):
    user = UserMapper.to_entity(request.json)
    user.id = user_id

    user_service.update(user)
    return jsonify(UserMapper.to_dto(user)), 200


@user_controller.route("/", methods=["GET"])
@jwt_required()
def current_user(user_service: UserService):
    user = user_service.get_current_user()
    return jsonify(UserMapper.to_dto(user)), 200

