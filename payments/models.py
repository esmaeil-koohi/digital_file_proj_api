from django.db import models
from utils.validators import validate_phone_number


class Gateway(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='gateways/')
    is_enable = models.BooleanField(default=True)
    # credentials = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID, 'Void'),
        (STATUS_PAID, 'Paid'),
        (STATUS_ERROR, 'Error'),
        (STATUS_CANCELED, 'User Canceled'),
        (STATUS_REFUNDED, 'Refunded'),
    )

    STATUS_TRANSLATIONS = {
        STATUS_VOID: 'Payment could not be processed',
        STATUS_PAID: 'Payment successful',
        STATUS_ERROR: 'Payment has encountered an error. Our technical team will check the problem shortly',
        STATUS_CANCELED: 'Payment canceled by user.',
        STATUS_REFUNDED: 'This payment has been refunded',
    }

    user = models.ForeignKey('user.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey('subscriptions.Package', related_name='%(class)s', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, related_name='%(class)s', on_delete=models.CASCADE)
    price = models.PositiveIntegerField('price', default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_VOID, db_index=True)
    device_uuid = models.CharField(max_length=40, blank=True)
    token = models.CharField(max_length=800)
    phone_number = models.BigIntegerField(validators=[validate_phone_number], db_index=True)
    consumed_code = models.PositiveIntegerField(null=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
