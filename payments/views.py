import razorpay
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Donation, PaymentLog
from rest_framework.viewsets import ModelViewSet
from .serializers import DonationSerializer, PaymentLogSerializer
import stripe
import requests


import json
from django.views.decorators.csrf import csrf_exempt


class DonationViewSet(ModelViewSet):
    queryset = Donation.objects.all().order_by("-created_at")
    serializer_class = DonationSerializer

class PaymentLogViewSet(ModelViewSet):
    queryset = PaymentLog.objects.all().order_by("-created_at")
    serializer_class = PaymentLogSerializer



# Initialize Razorpay client with your real keys
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
@api_view(['POST'])
def create_order_razorpay(request):
    try:
        amount = request.data.get("amount")
        print("Amount received:", amount)
        print("Razorpay keys:", settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)

        if not amount or int(amount) <= 0:
            return JsonResponse({"error": "Invalid or missing amount"}, status=400)

        amount_paise = int(amount) * 100

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        donation = Donation.objects.create(
            donor_name=request.data.get("donor_name", ""),
            donor_email=request.data.get("donor_email", ""),
            amount=amount,
            currency="INR",
            provider="razorpay",
            order_id=order["id"],
            status="created"
        )

        return JsonResponse({"order": order, "donation_id": donation.id})

    except Exception as e:
        import traceback
        print("Razorpay error:", traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=400)


@api_view(['POST'])
def verify_payment_razorpay(request):
    razorpay_order_id = request.data.get("order_id")
    razorpay_payment_id = request.data.get("payment_id")
    razorpay_signature = request.data.get("signature")

    try:
        # Verify signature using Razorpay utility
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        # Update donation record
        donation = Donation.objects.get(order_id=razorpay_order_id)
        donation.payment_id = razorpay_payment_id
        donation.status = "success"
        donation.save()

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)

def home(request):
    return HttpResponse("Welcome to the NGO CMS API")


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
def create_order_stripe(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = int(request.data.get("amount", 0)) * 100  # convert to cents

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Donation'},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )

        # ✅ Return sessionId consistently
        return JsonResponse({"sessionId": session.id})
    except Exception as e:
        print("Stripe error:", e)
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def webhook_stripe(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # add this to your .env

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        donation_id = session.get("client_reference_id")
        if donation_id:
            try:
                donation = Donation.objects.get(id=donation_id)
                donation.status = "success"
                donation.payment_id = session.get("payment_intent")
                donation.provider = "stripe"
                donation.save()
            except Donation.DoesNotExist:
                pass

    return HttpResponse(status=200)



# Helper: Get PayPal access token
def get_paypal_access_token():
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=auth
    )
    return response.json().get("access_token")

@api_view(['POST'])
def create_order_paypal(request):
    try:
        amount = request.data.get("amount")
        if not amount or float(amount) <= 0:
            return JsonResponse({"error": "Invalid or missing amount"}, status=400)

        donor_name = request.data.get("donor_name", "")
        donor_email = request.data.get("donor_email", "")

        access_token = get_paypal_access_token()
        if not access_token:
            return JsonResponse({"error": "Failed to get PayPal access token"}, status=400)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        order_payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",  # sandbox usually supports USD
                    "value": str(amount)
                }
            }]
        }

        response = requests.post(
            "https://api-m.sandbox.paypal.com/v2/checkout/orders",
            json=order_payload,
            headers=headers
        )
        order = response.json()
        print("PayPal response:", order)  # log full response

        if "id" not in order:
            return JsonResponse({"error": order}, status=400)

        donation = Donation.objects.create(
            donor_name=donor_name,
            donor_email=donor_email,
            amount=amount,
            currency="USD",
            provider="paypal",
            order_id=order["id"],
            status="created"
        )

        return JsonResponse({"order": order, "donation_id": donation.id})
    except Exception as e:
        import traceback
        print("PayPal error:", traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=400)


@api_view(['POST'])
def verify_payment_paypal(request):
    order_id = request.data.get("order_id")
    access_token = get_paypal_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Capture payment
    response = requests.post(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture",
        headers=headers
    )
    capture = response.json()

    try:
        donation = Donation.objects.get(order_id=order_id)
        if capture.get("status") == "COMPLETED":
            donation.status = "success"
            donation.payment_id = capture["purchase_units"][0]["payments"]["captures"][0]["id"]
        else:
            donation.status = "failed"
        donation.save()
    except Donation.DoesNotExist:
        pass

    return JsonResponse({"capture": capture})






@api_view(['POST'])
def verify_payment_razorpay(request):
    razorpay_order_id = request.data.get("order_id")
    razorpay_payment_id = request.data.get("payment_id")
    razorpay_signature = request.data.get("signature")

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        donation = Donation.objects.get(order_id=razorpay_order_id)
        donation.payment_id = razorpay_payment_id
        donation.status = "success"
        donation.save()

        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "failed"})
