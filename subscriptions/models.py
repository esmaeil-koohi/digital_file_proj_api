from django.db import models
from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(max_length=50)
    sku = models.CharField(max_length=20, db_index=True, validators=[validate_sku])
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='packages/')
    is_enable = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    duration = models.DurationField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='%(class)s')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
