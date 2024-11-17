from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Referral
import json
import string
import random

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["email", "name", "mobile_number", "city", "password"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({"error": f"Missing or invalid field: {field}"}, status=400)
            
            if "referral_code" in data and data["referral_code"]:
                referrer = User.objects.filter(referral_code=data["referral_code"]).first()
                if not referrer:
                    return JsonResponse({"error": "Invalid referral code"}, status=400)
            else:
                referrer = None

            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user = User.objects.create(
                email=data["email"],
                name=data["name"],
                mobile_number=data["mobile_number"],
                city=data["city"],
                password=make_password(data["password"]),
                referral_code=referral_code,
                referred_by=referrer.referral_code if referrer else None
            )
            
            Referral.objects.create(referrer=user, referee=user)
            
            return JsonResponse({"message": "User registered successfully", "referral_code": referral_code}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.filter(email=data["email"]).first()
            if user and check_password(data["password"], user.password):
                return JsonResponse({"user_id": user.id, "email": user.email}, status=200)
            return JsonResponse({"error": "Invalid email or password"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
def referrals(request):
    if request.method == "GET":
        referral_code = request.GET.get("referral_code")
        user = User.objects.filter(referral_code=referral_code).first()
        if not user:
            return JsonResponse({"error": "Invalid referral code"}, status=404)
        
        referrals = Referral.objects.filter(referrer=user)
        result = [
            {
                "name": r.referee.name,
                "email": r.referee.email,
                "registered_at": r.referee.created_at
            }
            for r in referrals
        ]
        return JsonResponse({"referrals": result}, status=200)