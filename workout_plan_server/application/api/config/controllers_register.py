from flask import Flask

from workout_plan_server.application.api.controllers.exercise_controller import exercise_controller
from workout_plan_server.application.api.controllers.training_controller import training_controller
from workout_plan_server.application.api.controllers.user_controller import user_controller
from workout_plan_server.application.api.controllers.workout_plan_controller import workout_plan_controller


def register_controllers(app: Flask):
    app.register_blueprint(exercise_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(workout_plan_controller)
    app.register_blueprint(training_controller)
