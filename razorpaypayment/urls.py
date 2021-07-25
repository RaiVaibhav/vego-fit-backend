# urls.py
from django.urls import path, include

from .views import *

urlpatterns = [
    path('create-order/', start_payment, name="payment"),
    path('payment/success/', handle_payment_success, name="payment_success"),
    path('addresspincode/<str:pincode>', get_pincode_detail)
]