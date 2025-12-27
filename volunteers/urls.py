from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerViewSet, EventViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r"volunteers", VolunteerViewSet, basename="volunteer")
router.register(r"events", EventViewSet, basename="event")

# Include router URLs
urlpatterns = [
    path("", include(router.urls)),
]
