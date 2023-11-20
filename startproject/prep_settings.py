# Python Standard Library Imports
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
    "core",
"""

    file_text = re.sub(apps_pattern, f"INSTALLED_APPS = [{apps}]", file_text)
    file_text = re.sub(middleware_pattern, f"MIDDLEWARE = [{middlewares}]", file_text)
    file_text = file_text.replace(
        "from pathlib import Path",
        "import re\nfrom pathlib import Path\nfrom decouple import config\nfrom utils.inertia_utils.inertia_json_encoder import InertiaCustomJsonEncoder",
    )
    file_text = re.sub(r"SECRET_KEY = .*", 'SECRET_KEY = config("SECRET_KEY")', file_text)
    file_text = file_text.replace(
        "DEBUG = True",
        'DEBUG = config("DEBUG", True, cast=bool)\nSSR_ENABLED = config("SSR_ENABLED", not DEBUG, cast=bool)',
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
}}

# User Model
AUTH_USER_MODEL = "core.User"
""".format(
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
        "LAYOUT": "index.html" if not SSR_ENABLED else "index_prod.html",
        "SSR_URL": config("SSR_URL", default="http://localhost:13714"),
        "SSR_ENABLED": SSR_ENABLED,
    },
    "DJANGO_VITE": {
        "DEV_MODE": DEBUG,  # vite dev mode, default based on django DEBUG
        "SERVER_PROTOCOL": "http",
        "DEV_SERVER_HOST": "localhost",
        "DEV_SERVER_PORT": 5173,
        "WS_CLIENT_URL": "@vite/client",
        "ASSETS_PATH": "static/dist",  # vite build asset path
        "STATIC_URL_PREFIX": "",
        "MANIFEST_PATH": "static/dist/manifest.json",
    },
}

# CSRF
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"

# Migrations
MIGRATION_PATH_DICT = {
    "PRODUCTION": "migrations",
    "STAGING": "migrations_staging",
}

ENVIRONMENT = config("ENVIRONMENT", default="LOCAL")
MIGRATION_PATH = MIGRATION_PATH_DICT.get(ENVIRONMENT, "migrations_dev")
MIGRATION_MODULES = {
    "core": "core." + MIGRATION_PATH,
}

# Inertia Encoder
INERTIA_JSON_ENCODER = InertiaCustomJsonEncoder

def immutable_file_test(path, url):
    # Match filename with 12 hex digits before the extension
    # e.g. app.db8f2edc0c8a.js
    return re.match(r"^.+\.[0-9a-f]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="")
if DEBUG:
    EMAIL_HOST = "mailpit"
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
    },
}
"""
    with open(f"./{project_name}/settings.py", "w") as file:
        file.write(file_text)
