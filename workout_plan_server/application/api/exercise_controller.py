from flask_restx import Resource

from workout_plan_server.application.api import exercise_namespace as ns


@ns.route("/<string:exercise_id>")
@ns.response(404, "Exercise not found")
class ExerciseController(Resource):

    @ns.doc("get_exercise")
    @ns.param("exercise_id", "Exercise id")
    def get(self, exercise_id: str):
        print(f"exercise_id: {exercise_id}")

        return{
            "id": "1",
            "name": "test"
        }

