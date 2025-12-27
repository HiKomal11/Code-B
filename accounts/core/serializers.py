from rest_framework import serializers
from .models import NGOProfile
from .models import Media
from .models import Subscription
from .models import CampaignParticipation, Campaign
class NGOProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOProfile
        fields = "__all__"


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
