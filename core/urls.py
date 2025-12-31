from django.urls import path, include
from .views import contact_message, SiteContentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'site-content', SiteContentViewSet, basename='sitecontent')

urlpatterns = [
    path("api/contact/", contact_message, name="contact_message"),
    path("api/", include(router.urls)),  
]
