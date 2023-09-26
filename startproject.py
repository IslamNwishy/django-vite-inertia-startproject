import argparse
import os
import re
import subprocess

from django.core.management.utils import get_random_secret_key


def prep_settings(project_name):
    with open(f"./{project_name}/settings.py", "r") as file:
        file_text = file.read()

    apps_pattern = re.compile(r"INSTALLED_APPS = \[([\s\S]*?)\]")
    middleware_pattern = re.compile(r"MIDDLEWARE = \[([\s\S]*?)\]")

    apps = re.search(apps_pattern, file_text).group(1)
    middlewares = re.search(middleware_pattern, file_text).group(1).split(",")[:-1]

    middlewares.insert(1, '''\n    "whitenoise.middleware.WhiteNoiseMiddleware"''')
    middlewares.append('''\n    "inertia.middleware.InertiaMiddleware"''')
    middlewares = ",".join(middlewares) + ",\n"

    apps += """    "django_breeze",
        "inertia",
    """

    file_text = re.sub(apps_pattern, f"INSTALLED_APPS = [{apps}]", file_text)
    file_text = re.sub(middleware_pattern, f"MIDDLEWARE = [{middlewares}]", file_text)
    file_text = file_text.replace(
        "from pathlib import Path\n",
        "from pathlib import Path\nfrom decouple import config",
    )
    file_text = re.sub(
        r"SECRET_KEY = .*", 'SECRET_KEY = config("SECRET_KEY")', file_text
    )
    file_text = file_text.replace(
        "DEBUG = True", 'DEBUG = config("DEBUG", True, cast=bool)'
    )
    file_text = file_text.replace(
        "ALLOWED_HOSTS = []",
        'ALLOWED_HOSTS = config("ALLOWED_HOSTS", "*").replace(" ","").split(",")',
    )
    file_text = re.sub(
        r"DATABASES = \{([\s\S]*?)\}",
        """
DATABASES = {{
    "default": {{
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="{project_name}"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASS", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }},
}}""".format(
            project_name=project_name
        ),
        file_text,
    )

    file_text = file_text.replace(
        "STATIC_URL = 'static/'",
        """
STATIC_URL = "static/"
STATIC_ROOT = "static"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

""",
    )

    file_text += """
# django-breeze configurations
DJANGO_BREEZE = {
    "INERTIA": {
        "LAYOUT": "index.html",
        "SSR_URL": "http://localhost:13714",
        "SSR_ENABLED": False,
    },
    "DJANGO_VITE": {
        "DEV_MODE": DEBUG,  # vite dev mode, default based on django DEBUG
        "SERVER_PROTOCOL": "http",
        "DEV_SERVER_HOST": "localhost",
        "DEV_SERVER_PORT": 5173,
        "WS_CLIENT_URL": "@vite/client",
        "ASSETS_PATH": "static/dist",  # vite build asset path
        "STATIC_URL_PREFIX": "",
    },
}
"""
    with open(f"./{project_name}/settings.py", "w") as file:
        file.write(file_text)


parser = argparse.ArgumentParser(
    description="Create a project django + vite (react + tailwind) + inertia"
)
parser.add_argument("project_name", nargs="?")
args = parser.parse_args()
project_name = args.project_name
if not project_name:
    raise ValueError(
        "You need to provide a project name follow (python ./startproject.py <project_name>)"
    )


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

# Prepare Settings
prep_settings(project_name)

# Create Front end
subprocess.run(["django-breeze", "create-app", "react"])
with open("vite.config.js", "w+") as file:
    file.write(file.read().replace('host: "localhost"', "host: true"))


with open(".env.sample", "r") as file:
    env_details = file.read()

env_details = env_details.replace("<project_name>", project_name)
env_details = env_details.replace("<Secret_KEY>", get_random_secret_key())

with open(".env", "w") as file:
    file.write(env_details)
try:
    os.removedirs(".git")
except:
    pass
subprocess.run(["git", "init"])

print(
    f"Your {project_name} project was initialized successfully!\nYou should delete startproject.py as it is no longer needed"
)
