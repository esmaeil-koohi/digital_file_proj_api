from django.db import models
from utils.validators import validate_phone_number


# class Gateway(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField(blank=True)
#     avatar = models.ImageField(upload_to='gateways/', blank=True)
#     is_enabled = models.BooleanField(default=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)
#
#
# class Payment(models.Model):
