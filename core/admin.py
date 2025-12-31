from django.contrib import admin
from .models import NGOProfile   
from .models import ContactMessage
from .models import Campaign, CampaignParticipation, Subscription
from .models import SiteContent

admin.site.register(NGOProfile)

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("title", "mission", "vision", "story_intro", "banner_image")
        }),
        ("Additional Info", {
            "fields": ("core_values", "programs")
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email", "message")


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer_name", "goal_amount", "created_at")
    search_fields = ("title", "organizer_name", "description")

@admin.register(CampaignParticipation)
class CampaignParticipationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "campaign", "joined_at")
    search_fields = ("name", "email")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subscribed_at")
    search_fields = ("email", "name")
