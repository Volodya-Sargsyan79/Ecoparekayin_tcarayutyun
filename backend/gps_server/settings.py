import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "back.settings"
)

django.setup()