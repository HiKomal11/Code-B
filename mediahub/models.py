from django.db import models

class Media(models.Model):
    MEDIA_TYPES = (
        ("photo", "Photo"),
        ("video", "Video"),
        ("press", "Press Release"),
    )
    type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.FileField(upload_to="media/")
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.caption}"
