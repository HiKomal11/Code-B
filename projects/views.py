from rest_framework import viewsets
from .models import ProjectParticipation, WorkArea
from .serializers import ProjectParticipationSerializer, WorkAreaSerializer


class ProjectParticipationViewSet(viewsets.ModelViewSet):
    queryset = ProjectParticipation.objects.all()
    serializer_class = ProjectParticipationSerializer

class WorkAreaViewSet(viewsets.ModelViewSet):
    queryset = WorkArea.objects.all()
    serializer_class = WorkAreaSerializer
