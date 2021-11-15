import os


def get_project_dir() -> str:
    dir_path = os.getcwd()
    path_github_action = "/github/workspace"
    path_github_action_with_tests = path_github_action + "/tests"

    if path_github_action_with_tests in dir_path:
        dir_path = path_github_action + dir_path.split(path_github_action_with_tests)[1]

    result = dir_path.split("workout-plan-server")[0] + "workout-plan-server"

    return result
