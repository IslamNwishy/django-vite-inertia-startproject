# Python Standard Library Imports
import argparse
import os
import subprocess
import sys

# Other Third Party Imports
from prep_backend import prep_backend
from prep_env import prep_env
from prep_frontend import prep_frontend
from prep_settings import prep_settings


def start_project():
    parser = argparse.ArgumentParser(description="Create a project django + vite (react + tailwind) + inertia")
    parser.add_argument("project_name", nargs="?")
    parser.add_argument("-f", "--front", default="vue3", choices=["react", "vue3"])
    args = parser.parse_args()
    project_name = args.project_name
    if not project_name:
        raise ValueError("You need to provide a project name follow (python ./startproject.py <project_name>)")

    # create project
    subprocess.run(["django-breeze", "startproject", project_name])
    source = f"./{project_name}__temp"
    os.rename(project_name, source)

    # gather all files
    allfiles = os.listdir(source)

    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(".", f)
        os.rename(src_path, dst_path)
    os.removedirs(source)

    subprocess.run([sys.executable, "manage.py", "startapp", "core"])

    # prep backend
    prep_backend()

    # Prepare Settings
    prep_settings(project_name)

    # Create Front end
    prep_frontend(args.front)

    # prep env
    prep_env(project_name)

    print(
        f"\nYour {project_name} project was initialized successfully!\nYou should delete startproject directory as it is no longer needed"
    )
