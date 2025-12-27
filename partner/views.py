from rest_framework.viewsets import ModelViewSet
from .models import PartnerInquiry
from .serializers import PartnerInquirySerializer

class PartnerInquiryViewSet(ModelViewSet):
    queryset = PartnerInquiry.objects.all().order_by("-submitted_at")
    serializer_class = PartnerInquirySerializer
