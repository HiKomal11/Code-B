# donations/views.py
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create_order(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = int(float(request.data['amount']) * 100)
    order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})
    return Response(order)
