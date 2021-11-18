from flask import Flask
from flask_jwt import JWT, JWTError
from injector import Injector

from workout_plan_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from workout_plan_server.services.impl.user_service import UserService
from workout_plan_server.services.ports.user_repository import UserRepository


def fill_jwt_auth_functions(app: Flask, injector: Injector) -> JWT:

    def authenticate(login: str, password: str):
        user_service = injector.get(UserService)

        try:
            return user_service.authenticate(login, password)
        except InvalidCredentialsException as ex:
            raise JWTError("Invalid credentials", str(ex))

    def identity(payload: dict):
        user_repository = injector.get(UserRepository)
        user_id = payload.get("identity")
        return user_repository.find_by_id(user_id)

    return JWT(app, authenticate, identity)
