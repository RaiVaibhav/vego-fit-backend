# Generated by Django 3.2.4 on 2021-06-11 08:07

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_product', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('order_amount', models.FloatField()),
                ('order_currency', models.CharField(default='INR', max_length=3)),
                ('order_notes', models.TextField(default='')),
                ('order_address', models.TextField()),
                ('order_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('isPaid', models.BooleanField(default=False)),
                ('order_created_at', models.BigIntegerField()),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('customer_phone_number', models.BigIntegerField()),
                ('razorpay_payment_id', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
