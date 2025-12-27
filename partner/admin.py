from django.contrib import admin
from .models import PartnerInquiry

@admin.register(PartnerInquiry)
class PartnerInquiryAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person", "email", "submitted_at")
    search_fields = ("company_name", "contact_person", "email")
