from django.apps import apps
from django.contrib import admin
from apps.common.models.base import *
from import_export.admin import ImportExportModelAdmin
"""
def register_all_models(app_label):
    app_config = apps.get_app_config(app_label)
    models = app_config.get_models()
    for model in models:
        try:  # noqa
            admin.site.register(model, ImportExportModelAdmin)
        except admin.sites.AlreadyRegistered:
            pass


register_all_models('common')

"""

def register_all_models():

    models = apps.get_models()
    for model in models:
        try:  # noqa
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


# Register all Models
register_all_models()