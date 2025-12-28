from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Ensure admin user is staff and superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        u, created = User.objects.get_or_create(username="admin", defaults={
            "email": "admin@example.com"
        })
        u.is_staff = True
        u.is_superuser = True
        u.set_password("Admin@123")
        u.save()
        self.stdout.write(self.style.SUCCESS("Admin user updated with staff/superuser flags"))
