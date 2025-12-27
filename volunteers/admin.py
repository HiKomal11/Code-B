from django.contrib import admin
from .models import Volunteer, Event   # only volunteer/event models

admin.site.register(Volunteer)
admin.site.register(Event)
