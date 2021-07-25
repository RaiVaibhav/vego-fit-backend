from django.core.validators import validate_email
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order