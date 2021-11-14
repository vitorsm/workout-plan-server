from flask import Flask
from flask_restx import Api

app = Flask(__name__)
workout_plan_api = Api(app, version="1.0", title="Workout plan API",
                       description="The workout plan API provides function to manage workout plans")

exercise_namespace = workout_plan_api.namespace("exercise", description="Exercise controller")
