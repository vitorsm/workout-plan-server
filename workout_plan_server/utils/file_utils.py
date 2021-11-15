import os


def get_project_dir() -> str:
    # /home/runner/work/workout-plan-server/workout-plan-server/tests/integration_tests/base_test.py

    dir_path = os.getcwd()
    result = dir_path.split("workout-plan-server")[0] + "workout-plan-server"

    if "/home/runner/work/workout-plan-server" in result:
        result += "/workout-plan-server"

    return result
