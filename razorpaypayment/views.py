import json
from os import error
import pdb

import razorpay
from django.conf import settings
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

geolocator = Nominatim(user_agent="getpincode")

@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    order_product = request.data['order_product']
    currency = request.data['currency'] if 'currency' in request.data else 'INR'
    notes = request.data['notes'] if 'notes' in request.data else None
    customer_name = request.data['customer_name']
    customer_phone_number = request.data['customer_phone_number']
    customer_email = request.data['customer_email']
    order_address = request.data['order_address']
    order_notes = request.data['notes']

    # setup razorpay client
    client = razorpay.Client(
        auth=(settings.RAZOR_PUBLIC_KEY, settings.RAZOR_SECRET_KEY))
    # create razorpay order

    data = dict(order_product=order_product,
                order_amount=amount,
                customer_name=customer_name,
                customer_phone_number=customer_phone_number,
                customer_email=customer_email,
                order_currency=currency,
                order_address=order_address,
                order_notes=order_notes)
    try:
        serializer = OrderSerializer(data=data)
        try:
            payment = client.order.create(dict(amount=(int(amount) * 100), currency=currency,
                                            payment_capture=1, notes={'Additional Info': order_notes} if order_notes else dict()))
        except Exception as e:
            return Response({'message': 'Something went wrong in creating a order'}, status=status.HTTP_400_BAD_REQUEST)
        data['order_id'] = payment['id']
        data['order_created_at'] = payment['created_at']
    except:
        return Response(status=400, data={'message': 'Something went wrong in creating a order'})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    data = request.data
    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    """
    order = Order.objects.get(order_id=data['razorpay_order_id'])
    client = razorpay.Client(
        auth=(settings.RAZOR_PUBLIC_KEY, settings.RAZOR_SECRET_KEY))

    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.razorpay_payment_id = data['razorpay_payment_id']
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)

@api_view(['GET'])
def get_pincode_detail(request, pincode):
    try:
        location = geolocator.geocode(str(pincode), addressdetails=True, language='en')
    except:
        return Response({'message': 'Something went wrong in fetching the detail from pincode'}, status=status.HTTP_400_BAD_REQUEST)
    if location:
        address = location.raw['address']
        return Response(address)
    return Response({'message': 'no data found'}, status=status.HTTP_404_NOT_FOUND)
