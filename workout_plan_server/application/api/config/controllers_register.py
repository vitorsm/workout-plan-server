from flask import Flask

from workout_plan_server.application.api.controllers.exercise_controller import exercise_controller
from workout_plan_server.application.api.controllers.user_controller import user_controller


def register_controllers(app: Flask):
    app.register_blueprint(exercise_controller)
    app.register_blueprint(user_controller)
