from flask import Blueprint, jsonify
from flask_jwt import JWTError

from workout_plan_server.application.api.mapper.error_mapper import ErrorMapper
from workout_plan_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException
from workout_plan_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from workout_plan_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.log import get_logger


logger = get_logger(__name__)


def fill_error_handlers_to_controller(controller: Blueprint):

    @controller.errorhandler(JWTError)
    def invalid_entity_exception(exception: JWTError):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 401)), 401

    @controller.errorhandler(PermissionException)
    def invalid_entity_exception(exception: PermissionException):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 403)), 403

    @controller.errorhandler(InvalidEntityException)
    def invalid_entity_exception(exception: InvalidEntityException):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 400)), 400

    @controller.errorhandler(DuplicateEntityException)
    def duplicate_entity_exception(exception: DuplicateEntityException):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 409)), 409

    @controller.errorhandler(EntityNotFoundException)
    def entity_not_found_exception(exception: EntityNotFoundException):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 404)), 404

    @controller.errorhandler(Exception)
    def generic_exception(exception: Exception):
        logger.exception(exception)
        return jsonify(ErrorMapper.to_dto(exception, 500)), 500
