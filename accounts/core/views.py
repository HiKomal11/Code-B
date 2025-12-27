# core/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Subscription, Campaign, CampaignParticipation, Media
from .serializers import SubscriptionSerializer, CampaignSerializer, CampaignParticipationSerializer, MediaSerializer
from rest_framework import status
from .models import ContactMessage
from rest_framework.permissions import AllowAny


def contact_message(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    # Save to DB or send email notification
    print(f"New message from {name} ({email}): {message}")

    return Response({"success": True, "message": "Message received!"})


@api_view(["GET", "POST"])
def subscribe(request):
    if request.method == "POST":
        data = request.data
        sub = Subscription.objects.create(
            name=data.get("name"),
            email=data.get("email"),
        )
        return Response({"message": "Subscription successful!"})
    elif request.method == "GET":
        subs = Subscription.objects.all().order_by("-subscribed_at")
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)



@api_view(["POST"])
def contact_message(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    ContactMessage.objects.create(name=name, email=email, message=message)

    return Response({"success": "Message saved!"}, status=status.HTTP_200_OK)


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all().order_by("-subscribed_at")
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

class CampaignParticipationViewSet(ModelViewSet):
    queryset = CampaignParticipation.objects.all().order_by("-joined_at")
    serializer_class = CampaignParticipationSerializer
    permission_classes = [AllowAny]

class CampaignViewSet(ModelViewSet):
    queryset = Campaign.objects.all().order_by("-created_at")
    serializer_class = CampaignSerializer
    permission_classes = [AllowAny]  

class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all().order_by("-uploaded_at")
    serializer_class = MediaSerializer


