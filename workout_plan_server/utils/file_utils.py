import os


def get_project_dir() -> str:
    dir_path = os.getcwd()
    path_github_action = "/github/workspace"
    path_github_action_with_tests = path_github_action + "/tests"

    is_github_action = path_github_action_with_tests in dir_path
    if is_github_action:
        dir_path = path_github_action + dir_path.split(path_github_action_with_tests)[1]

    result = dir_path.split("workout-plan-server")[0]

    if not is_github_action:
        result = result + "workout-plan-server"

    return result
