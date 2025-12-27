from rest_framework import serializers
from .models import ProjectParticipation
from .models import WorkArea
class ProjectParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectParticipation
        fields = "__all__"

class WorkAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkArea
        fields = "__all__"
