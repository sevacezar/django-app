from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'description',
            'price',
            'discount',
            'created_at',
            'archived',
            'preview',
            'created_by',
        )

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = (
            'pk',
            'delivary_address',
            'promocode',
            'created_at',
            'user',
            'products',
        )