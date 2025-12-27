from rest_framework import serializers
from .models import PartnerInquiry

class PartnerInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerInquiry
        fields = "__all__"
