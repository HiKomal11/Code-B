from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username", "email", "is_staff", "is_active", "is_superuser", "date_joined"
    )
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    # Fields shown when editing an existing user
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "is_superuser",   
            ),
        }),
    )
