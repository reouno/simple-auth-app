"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

import google.auth
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps
from google.cloud import secretmanager

from api_server.apps.custom_accounts.models import CustomUser


def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    if not os.getenv("RUN_CLOUD", None):
        pass
    else:
        client = secretmanager.SecretManagerServiceClient()

        # Get project value for identifying current context
        _, project = google.auth.default()

        # Retrieve the previously stored admin password
        PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "superuser_password")
        name = f"projects/{project}/secrets/{PASSWORD_NAME}/versions/latest"
        admin_password = client.access_secret_version(name=name).payload.data.decode(
            "UTF-8"
        )

        # Create a new user using acquired password, stripping any accidentally stored newline
        # characters
        CustomUser.objects.create_superuser("admin@example.com", password=admin_password.strip())


class Migration(migrations.Migration):
    """Migration definition"""
    dependencies = [('custom_accounts', '0001_initial')]
    operations = [migrations.RunPython(createsuperuser)]
