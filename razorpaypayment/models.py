  
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_email


# Create your models here.

class Order(models.Model):
    order_product = ArrayField(models.CharField(max_length=100, blank=False, null=False), blank=False, null=False)
    order_amount = models.FloatField(null=False, blank=False)
    order_currency = models.CharField(max_length=3, default='INR')
    order_notes = models.TextField(blank=True)
    order_address = models.TextField(null=False, blank=False)
    order_id = models.CharField(max_length=500, primary_key=True)
    isPaid = models.BooleanField(default=False)
    order_created_at = models.BigIntegerField(null=False, blank=False)
    customer_name = models.CharField(max_length=50,null=False, blank=False)
    customer_email = models.EmailField(validators=[validate_email], null=False, blank=False)
    customer_phone_number = models.CharField(max_length=20, null=False, blank=False)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=False)

    def __str__(self):
        return '-'.join(self.order_product)