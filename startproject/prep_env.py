# Python Standard Library Imports
import shutil
from pathlib import Path

# Django Imports
from django.core.management.utils import get_random_secret_key


def prep_env(project_name):
    with open(".env.sample", "r") as file:
        env_details = file.read()

    env_details = env_details.replace("<project_name>", project_name)
    env_details = env_details.replace("<Secret_KEY>", get_random_secret_key())

    with open(".env", "w") as file:
        file.write(env_details)
    Path("./static/dist/").mkdir(parents=True, exist_ok=True)
    Path("./src/public").mkdir(parents=True, exist_ok=True)
    file = open("./static/dist/.gitkeep", "w")
    file.close()
    file = open("./src/public/.gitkeep", "w")
    file.close()
    shutil.rmtree(".git", ignore_errors=True)
