from django.db import models

# Create your models here.
class UserCred(models.Model):
    user_id = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    last_login = models.DateTimeField(null=True)

class OTP(models.Model):
    user_id = models.EmailField(unique=True)

    otp = models.IntegerField()
    valid_till = models.DateTimeField()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
