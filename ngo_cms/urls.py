from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


from core.views import ping_db   # import the view




from volunteers.views import VolunteerViewSet
from payments.views import DonationViewSet, home
from core.views import contact_message
from blog.views import blog_list, blog_detail , BlogPostViewSet 
from partner.views import PartnerInquiryViewSet
from core.views import SubscriptionViewSet, CampaignParticipationViewSet, CampaignViewSet, MediaViewSet, auth_status
from projects.views import WorkAreaViewSet
from django.http import HttpResponse
from payments.views import register_view, login_view
def health_check(request):
    return HttpResponse("OK")



router = DefaultRouter()
router.register(r'volunteers', VolunteerViewSet, basename='volunteers')
router.register(r'donations', DonationViewSet, basename='donations')
router.register(r"partner-inquiries", PartnerInquiryViewSet, basename="partner-inquiry")
router.register(r"subscribe", SubscriptionViewSet, basename="subscription")
router.register(r"campaign-participation", CampaignParticipationViewSet, basename="campaign-participation")
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"media", MediaViewSet, basename="media")
router.register(r'work', WorkAreaViewSet)
router.register(r"blog", BlogPostViewSet, basename="blog")

urlpatterns = [
    path('', home),  # root URL
    path('admin/', admin.site.urls),

    # Router endpoints (volunteers + donations CRUD)
    path('api/', include(router.urls)),

    # Delegate to app-level urls
    path("api/payments/", include("payments.urls")),
    path("api/volunteers/", include("volunteers.urls")),
    path("api/contact/", contact_message, name="contact_message"),
    path("api/blog/", blog_list, name="blog_list"),
    path("api/blog/<int:pk>/", blog_detail, name="blog_detail"),
    path('api/', include('projects.urls')),
    path("api/", include("core.urls")),
    path("api/", include("accounts.urls")),
    path("health/", health_check, name="health_check"),
    path("ping/", ping_db),   
    path("api/auth/status/", auth_status, name="auth_status"),
    path("register/", register_view),
    path("login/", login_view),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)