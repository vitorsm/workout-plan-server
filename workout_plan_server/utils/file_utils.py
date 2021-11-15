import os


def get_project_dir() -> str:
    dir_path = os.getcwd()
    return dir_path.split("workout-plan-server")[0] + "workout-plan-server"
