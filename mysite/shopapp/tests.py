from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = ''.join(choices(ascii_letters, k=10))  # генерируем случайное имя продукта
        Product.objects.filter(name=self.product_name).delete()  # удаляем перед запуском тестов продукты с такими именами на всякий случай
        user = User(username='test', password='password')
        user.save()
    
    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {"name": self.product_name,
             "price": 123.45,
             "description": 'Good product',
             "discount": 10}
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        user = User(username='test', password='password')
        user.save()
        cls.product = Product.objects.create(name='Best product')


    # def setUp(self):
    #     self.product = Product.objects.create(name='Best product')

    
    # def tearDown(self):
    #     self.product.delete()
    
    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    
    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'users-fixture.json',
        'groups-fixture.json'
    ]
    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        ## way 1
        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        ## way 2
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context['object_list']  # 'object_list' in context of view function!
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        ## way 3
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context['object_list']],
            transform=lambda p: p.pk,  # обработка qs для сравнения с value
        )
        self.assertTemplateUsed(response, 'shopapp/product_list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='bob_test', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self):
        # self.client.login(**self.credentials) # логинимся
        self.client.force_login(self.user)  # way 2 for loging

    def test_order_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders') # если не будет доступа - мы не будем допущены к этой странице 

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)  
        # self.assertRedirects(response, str(settings.LOGIN_URL))  # не проходит, так как появляется в url "next"


# Test TDD
class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'users-fixture.json',
        'groups-fixture.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products-export'),
        )

        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived,
            }
            for product in products
        ]

        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )


# HOMEWORK
class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(username='Sarah_test', password='qwerty123456')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.order_data = {
            'delivary_address': 'Street',
            'promocode': 'test_promo',
        }
        self.client.force_login(self.user)
        self.order = Order(**self.order_data)
        self.order.user = self.user
        self.order.save()

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order_data.get('delivary_address'))
        self.assertContains(response, self.order_data.get('promocode'))
        self.assertEqual(response.context['object'].pk, self.order.pk)
    

class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'users-fixture.json',
        'groups-fixture.json',
        'orders-fixture.json',
        'contenttypes-fixture.json',
        'permissions-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='Antonio Banderas', password='comoestas')

        order_content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.create(
            codename='export_orders',
            content_type=order_content_type,
        )
        cls.user.user_permissions.add(permission)
        cls.user.save()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders-export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'delivary_address': order.delivary_address,
                'promocode': order.promocode,
                'username': order.user.username,
                'products': [
                    {
                        'name': product.name,
                        'price': str(product.price),
                    }
                    for product in order.products
                ]
            }
            for order in orders
            
        ]
        orders_data = response.json()
        self.assertEqual(orders_data.get('orders'), expected_data)
