from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .models import Volunteer, Event
from .serializers import VolunteerSerializer, EventSerializer

from rest_framework.permissions import AllowAny

class VolunteerViewSet(ModelViewSet):
    queryset = Volunteer.objects.all().order_by("-joined_at")
    serializer_class = VolunteerSerializer
    permission_classes = [AllowAny]  # ✅ anyone can create/read/update
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "interest_area", "skills"]
    ordering_fields = ["joined_at", "name"]


class EventViewSet(ModelViewSet):
    """
    API endpoint for managing events.
    """
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer
    permission_classes = [AllowAny] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "location"]  # ✅ allow searching
    ordering_fields = ["date", "title"]  # ✅ allow ordering by these fields
