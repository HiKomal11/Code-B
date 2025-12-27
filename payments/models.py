from django.db import models

class Donation(models.Model):
    donor_name = models.CharField(max_length=120, blank=True)
    donor_email = models.EmailField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')

    # 👇 NEW FIELD: identifies which payment gateway was used
    provider = models.CharField(
        max_length=20,
        choices=[
            ('razorpay', 'Razorpay'),
            ('stripe', 'Stripe'),
            ('paypal', 'PayPal'),
        ],
        default='razorpay'
    )

    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='created')  # created/success/failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency} via {self.provider}"
class PaymentLog(models.Model):
    provider = models.CharField(max_length=50)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20)
    raw_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
