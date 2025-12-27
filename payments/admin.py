from django.contrib import admin
from .models import Donation, PaymentLog

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor_name", "donor_email", "amount", "currency", "provider", "status", "created_at")
    search_fields = ("donor_name", "donor_email", "order_id", "payment_id")
    list_filter = ("provider", "status", "currency")

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ("provider", "order_id", "payment_id", "status", "created_at")
    search_fields = ("order_id", "payment_id")
    list_filter = ("provider", "status")
