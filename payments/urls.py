from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    DonationViewSet,
    PaymentLogViewSet,
    create_order_razorpay,
    verify_payment_razorpay,
    create_order_stripe,
    webhook_stripe,
    create_order_paypal,
    verify_payment_paypal,
)

# Router for standard CRUD endpoints
router = DefaultRouter()
router.register(r"donations", DonationViewSet)
router.register(r"payment-logs", PaymentLogViewSet)

# Custom payment endpoints
custom_urlpatterns = [
    path("razorpay/create-order/", create_order_razorpay),
    path("razorpay/verify/", verify_payment_razorpay),
    path("stripe/create-order/", create_order_stripe),
    path("stripe/webhook/", webhook_stripe),
    path("paypal/create-order/", create_order_paypal),
    path("paypal/verify/", verify_payment_paypal),
]

# Combine both
urlpatterns = router.urls + custom_urlpatterns
