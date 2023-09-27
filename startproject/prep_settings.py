import re


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
        "from pathlib import Path",
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
        r"DATABASES = \{([\s\S]*?)\}([\s\S]*?)\}",
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

# CSRF
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"
"""
    with open(f"./{project_name}/settings.py", "w") as file:
        file.write(file_text)
