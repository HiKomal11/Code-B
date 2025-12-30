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
router.register(r"donations", DonationViewSet, basename="donation")
router.register(r"payment-logs", PaymentLogViewSet, basename="paymentlog")

# Custom payment endpoints
custom_urlpatterns = [
    path("razorpay/create-order/", create_order_razorpay, name="create_order_razorpay"),
    path("razorpay/verify/", verify_payment_razorpay, name="verify_payment_razorpay"),
    path("stripe/create-order/", create_order_stripe, name="create_order_stripe"),
    path("stripe/webhook/", webhook_stripe, name="webhook_stripe"),
    path("paypal/create-order/", create_order_paypal, name="create_order_paypal"),
    path("paypal/verify/", verify_payment_paypal, name="verify_payment_paypal"),
]

# Combine router + custom endpoints
urlpatterns = custom_urlpatterns + router.urls
