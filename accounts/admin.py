from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Show these fields in the admin list view
    list_display = (
        "email", "username", "role", "is_staff", "is_active", "is_superuser", "date_joined"
    )
    list_filter = ("role", "is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    # Fields visible when editing an existing user
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "role")}),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields visible when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "is_superuser",
            ),
        }),
    )
