import io

import google.auth
import google.cloud.logging
from google.cloud import secretmanager

from .base import *

DEBUG = False

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
# ...
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")

ALLOWED_HOSTS = os.environ.get('HOSTS').split(',')
CORS_ALLOWED_ORIGINS = os.environ.get('ORIGINS').split(',')
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECRET_KEY = env("SECRET_KEY")

# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

SIMPLE_JWT = {
    'AUTH_HEADER_NAME': 'HTTP_X_FORWARDED_AUTHORIZATION',
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {pathname} {funcName} L{lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'cloud_logging': {
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': google.cloud.logging.Client(),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'root': {
        'handlers': ['cloud_logging', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['cloud_logging', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
