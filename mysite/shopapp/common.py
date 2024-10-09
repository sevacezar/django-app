import json
from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User
from django.db import transaction

from .models import Product, Order

def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
            file,
            encoding=encoding,
        )
    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


@transaction.atomic
def save_json_orders(file, encoding):
    json_file = TextIOWrapper(
        file,
        encoding=encoding
    )
    orders_dict = json.load(json_file)
    orders = []
    for order in orders_dict:
        user = User.objects.filter(id=order.get('user_id')).first()
        products = Product.objects.filter(id__in=order.get('products_ids')).all()
        order_obj = Order.objects.create(
            delivary_address=order.get('delivary_address'),
            promocode=order.get('promocode'),
            user=user,
        )
        order_obj.products.add(*products)
        order_obj.save()
        orders.append(order_obj)
    
    return orders
    