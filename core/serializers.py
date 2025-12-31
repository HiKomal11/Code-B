from rest_framework import serializers
from .models import NGOProfile
from .models import Media
from .models import Subscription, SiteContent
from .models import CampaignParticipation, Campaign
class NGOProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOProfile
        fields = "__all__"


class SiteContentSerializer(serializers.ModelSerializer):
    core_values = serializers.SerializerMethodField()
    programs = serializers.SerializerMethodField()

    class Meta:
        model = SiteContent
        fields = ["id", "title", "mission", "vision", "story_intro", "banner_image", "core_values", "programs", "updated_at"]

    def get_core_values(self, obj):
        return obj.core_values.split(";") if obj.core_values else []

    def get_programs(self, obj):
        return obj.programs.split(";") if obj.programs else []

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"


class CampaignParticipationSerializer(serializers.ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(queryset=Campaign.objects.all())
    campaign_detail = CampaignSerializer(source="campaign", read_only=True)
    class Meta:
        model = CampaignParticipation
        fields = "__all__" 


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
