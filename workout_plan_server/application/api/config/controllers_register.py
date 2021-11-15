from flask import Flask

from workout_plan_server.application.api.controllers.exercise_controller import exercise_controller


def register_controllers(app: Flask):
    app.register_blueprint(exercise_controller)
