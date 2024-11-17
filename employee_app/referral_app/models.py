from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=10, unique=True)
    referred_by = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name="referrer", on_delete=models.CASCADE)
    referee = models.ForeignKey(User, related_name="referee", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)