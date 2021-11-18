from workout_plan_server import configs
from workout_plan_server.application.api import app

if __name__ == "__main__":
    app.run("0.0.0.0", port=configs.HOST_PORT)
