from django.db import models

class ProjectParticipation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    project = models.CharField(max_length=200)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project}"


class WorkArea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="work_images/", blank=True, null=True)

    def __str__(self):
        return self.title
