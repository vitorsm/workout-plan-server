import os
import shutil
import zipfile


def get_project_dir() -> str:
    dir_path = os.getcwd()
    return dir_path.split("workout-plan-server")[0] + "workout-plan-server"


def unzip_file(zip_file_path: str, directory_path: str):
    create_directory(directory_path)

    with open(zip_file_path, 'rb') as file:
        zipshape = zipfile.ZipFile(file)
        zipshape.extractall(directory_path)


def create_directory(directory_path: str):
    parent_dir = os.path.dirname(directory_path)

    if not os.path.exists(parent_dir):
        create_directory(parent_dir)

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def delete_directory(directory_path: str, remove_children: bool = False):
    if os.path.exists(directory_path):

        if remove_children:
            shutil.rmtree(directory_path)
        else:
            os.rmdir(directory_path)


def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
