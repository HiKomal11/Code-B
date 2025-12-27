from django.contrib import admin
from django.conf import settings

admin.site.site_header = settings.PROJECT_NAME
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = f"Welcome to {settings.PROJECT_NAME} Dashboard"
