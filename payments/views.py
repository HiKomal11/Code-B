import razorpay
import stripe
import requests
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .models import Donation, PaymentLog
from .serializers import DonationSerializer, PaymentLogSerializer


class DonationViewSet(ModelViewSet):
    queryset = Donation.objects.all().order_by("-created_at")
    serializer_class = DonationSerializer


class PaymentLogViewSet(ModelViewSet):
    queryset = PaymentLog.objects.all().order_by("-created_at")
    serializer_class = PaymentLogSerializer


# ✅ Razorpay
@api_view(['POST'])
def create_order_razorpay(request):
    try:
        amount = request.data.get("amount")
        if not amount:
            return JsonResponse({"error": "Missing amount"}, status=400)

        try:
            amount = float(amount)   # handles "500.00"
        except ValueError:
            return JsonResponse({"error": "Invalid amount format"}, status=400)

        if amount <= 0:
            return JsonResponse({"error": "Amount must be greater than 0"}, status=400)

        amount_paise = int(amount * 100)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        donation = Donation.objects.create(
            donor_name=request.data.get("name", ""),
            donor_email=request.data.get("email", ""),
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
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
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
    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)


# ✅ Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_order_stripe(request):
    try:
        amount = request.data.get("amount")
        if not amount:
            return JsonResponse({"error": "Missing amount"}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"error": "Invalid amount format"}, status=400)

        if amount <= 0:
            return JsonResponse({"error": "Amount must be greater than 0"}, status=400)

        stripe_amount = int(amount * 100)  # convert to cents/paise

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',  # use INR if donations are in ₹
                    'product_data': {'name': 'Donation'},
                    'unit_amount': stripe_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://hikomal11.github.io/success',
            cancel_url='https://hikomal11.github.io/cancel',
        )

        return JsonResponse({"sessionId": session.id})
    except Exception as e:
        print("Stripe error:", e)
        return JsonResponse({"error": str(e)}, status=400)


# ✅ PayPal
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
        if not amount:
            return JsonResponse({"error": "Missing amount"}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"error": "Invalid amount format"}, status=400)

        if amount <= 0:
            return JsonResponse({"error": "Amount must be greater than 0"}, status=400)

        donor_name = request.data.get("name", "")
        donor_email = request.data.get("email", "")

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
                    "currency_code": "USD",
                    "value": f"{amount:.2f}"  # format to 2 decimals
                }
            }]
        }

        response = requests.post(
            "https://api-m.sandbox.paypal.com/v2/checkout/orders",
            json=order_payload,
            headers=headers
        )
        order = response.json()
        print("PayPal response:", order)

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
