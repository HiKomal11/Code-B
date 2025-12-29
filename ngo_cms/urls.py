from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from core.views import ping_db, contact_message, SubscriptionViewSet, CampaignParticipationViewSet, CampaignViewSet, MediaViewSet, auth_status
from volunteers.views import VolunteerViewSet
from payments.views import DonationViewSet, home
from blog.views import BlogPostViewSet
from partner.views import PartnerInquiryViewSet
from projects.views import WorkAreaViewSet
from payments.views import register_api, login_api, logout_api, about_view, contact_view

def health_check(request):
    return HttpResponse("OK")

router = DefaultRouter()
router.register(r'volunteers', VolunteerViewSet, basename='volunteers')
router.register(r'donations', DonationViewSet, basename='donations')
router.register(r'partner-inquiries', PartnerInquiryViewSet, basename='partner-inquiry')
router.register(r'subscribe', SubscriptionViewSet, basename='subscription')
router.register(r'campaign-participation', CampaignParticipationViewSet, basename='campaign-participation')
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'work', WorkAreaViewSet)
router.register(r'blog', BlogPostViewSet, basename='blog')

urlpatterns = [
    path('', home),  # root URL
    path('admin/', admin.site.urls),

    # Router endpoints
    path('api/', include(router.urls)),

    # Delegate to app-level urls
    path("api/payments/", include("payments.urls")),
    path("api/contact/", contact_message, name="contact_message"),
    path("api/", include("projects.urls")),
    path("api/", include("core.urls")),
    path("api/", include("accounts.urls")),

    # Health + diagnostics
    path("health/", health_check, name="health_check"),
    path("ping/", ping_db),
    path("api/auth/status/", auth_status, name="auth_status"),

    # Authentication API (for React frontend)
    path("api/register/", register_api),
    path("api/login/", login_api),
    path("api/logout/", logout_api),

    # Optional static pages
    path("about/", about_view),
    path("contact/", contact_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
