from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('sales', 'Salesperson'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)  # enforce unique email
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = "email"   # login with email
    REQUIRED_FIELDS = ["username"]  # still require username for admin convenience

    def __str__(self):
        return self.email
