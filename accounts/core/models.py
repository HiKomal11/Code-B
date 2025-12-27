from django.db import models
from django.utils.translation import gettext_lazy as _

class NGOProfile(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    mission = models.TextField(verbose_name=_("Mission"))
    vision = models.TextField(verbose_name=_("Vision"))
    history = models.TextField(blank=True, null=True, verbose_name=_("History"))
    logo = models.ImageField(upload_to="core/", blank=True, null=True, verbose_name=_("Logo"))

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    organizer_name = models.CharField(max_length=100, default="Unknown")
 
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class CampaignParticipation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} joined {self.campaign.title}"

class Media(models.Model):
    MEDIA_TYPES = [
        ("photo", "Photo"),
        ("video", "Video"),
        ("press", "Press Coverage"),
        ("blog", "Blog/News"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    url = models.URLField(blank=True, null=True)   # link to video, blog, press article
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type})"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
