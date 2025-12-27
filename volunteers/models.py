from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)  # ✅ prevent duplicate registrations
    phone = models.CharField(max_length=15, blank=True, null=True)
    interest_area = models.CharField(max_length=200, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # ✅ extra detail
    availability = models.CharField(max_length=100, blank=True, null=True)  # ✅ e.g. weekends, evenings
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    volunteers = models.ManyToManyField(Volunteer, blank=True, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ track when event was added
    updated_at = models.DateTimeField(auto_now=True)      # ✅ track changes

    def __str__(self):
        return f"{self.title} on {self.date}"
