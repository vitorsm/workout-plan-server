from flask import Blueprint


controller = Blueprint("exercise_controller", __name__, url_prefix="/v1/exercise")

@controller.route("/")
def find_all():
