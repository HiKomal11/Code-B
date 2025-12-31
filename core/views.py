from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from .models import Subscription, Campaign, CampaignParticipation, Media, ContactMessage,  SiteContent
from .serializers import SubscriptionSerializer, CampaignSerializer, CampaignParticipationSerializer, MediaSerializer, SiteContentSerializer


@api_view(["GET"])
def auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"is_authenticated": True, "username": request.user.username})
    return JsonResponse({"is_authenticated": False})

@api_view(["GET"])
def ping_db(request):
    try:
        User = get_user_model()
        count = User.objects.count()
        return HttpResponse(f"✅ DB is connected. Users in DB: {count}")
    except Exception as e:
        return HttpResponse(f"❌ DB error: {str(e)}")

@api_view(["POST"])
def contact_message(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    ContactMessage.objects.create(name=name, email=email, message=message)
    return Response({"success": "Message saved!"}, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def subscribe(request):
    if request.method == "POST":
        data = request.data
        sub = Subscription.objects.create(
            name=data.get("name"),
            email=data.get("email"),
        )
        return Response({"message": "Subscription successful!"})
    else:
        subs = Subscription.objects.all().order_by("-subscribed_at")
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only admins can edit, others can read.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class SiteContentViewSet(viewsets.ModelViewSet):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [AllowAny]
