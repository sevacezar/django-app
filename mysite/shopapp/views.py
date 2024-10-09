"""
В модуле находятся различныенаборы представлений.

Разные представления интернет-магазина: по товарам, заказам и т.д.
"""
import time
import logging
from random import random
from typing import Any
from csv import DictWriter

from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .common import save_csv_products
from .forms import OrderForm, GroupForm, ProductForm
from .serializers import ProductSerializer, OrderSerializer
from shopapp.models import Product, Order, ProductImage

log = logging.getLogger(__name__)

# Create your views here.
@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Пoлный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        # DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    # filterset_fields = [
    #     'name',
    #     'description',
    #     'price',
    #     'discount',
    #     'archived',
    # ]
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]

    @extend_schema(
            summary='Get one product by id',
            description='**Retrieves** products, 404 if not found',
            responses={
                200: ProductSerializer,
                404: OpenApiResponse(description='Empty response, product by id not found'),
            })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @action(methods=['get'], detail=False,)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Desposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)

        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow(
                {
                    field: getattr(product, field)
                    for field in fields
                }
            )
        return response
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            file=request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['delivary_address']
    ordering_fields = [
        'delivary_address',
        'created_at',
    ]


class ShopIndexView(View):
    # @method_decorator(cache_page(10))
    def get(self, request: HttpRequest) -> HttpResponse: 
        context = {
            'refs': [
                {'name': 'products/', 'description': 'List of products'},
                {'name': 'orders/', 'description': 'List of orders'},
                ]
                }
        log.debug('Refs for shop index: %s', context['refs'])
        log.info('Rendering shop index')

        print('shop index context', context)  # for cache testing
        return render(
            request=request,
            template_name='shopapp/shop-index.html',
            context=context
        )
    
class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request=request, template_name='shopapp/groups-list.html', context=context)
    
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)
    
class ProductDetailView(DetailView):
    # model = Product
    queryset = Product.objects.prefetch_related('images')


class ProductsListView(ListView):
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(
    # PermissionRequiredMixin,
    CreateView,
    ):
    # permission_required = 'shopapp.add_product'

    model = Product
    fields = "name", "price", "description", "discount", 'preview'
    success_url = reverse_lazy('shopapp:products_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

class ProductUpdateView(
    UserPassesTestMixin,
    UpdateView,
    ):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        has_permission = self.request.user.has_perm('shopapp.change_product')
        product = self.get_object()
        if has_permission and product.created_by == self.request.user:
            return True
        return False

    model = Product
    # fields = "name", "price", "description", "discount", 'preview'
    form_class = ProductForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

    def form_valid(self, form):
        """For adding multiple images choice"""
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

class ProductArchiveView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        # .select_related('user')
        # .prefetch_related('products').all()
        .all()
    )

class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet[Any]:
        user_id = self.kwargs.get('user_id')
        user = User.objects.filter(id=user_id)
        if not user:
            raise Http404(f'Пользователь с id {user_id} не найден.')
        orders = Order.objects.filter(user_id=user_id).prefetch_related('products')
        self.owner = user
        return orders
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context




class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['shopapp.view_order']
    queryset = Order.objects.select_related('user').prefetch_related('products').all()


class OrderCreateView(CreateView):
    model = Product
    form_class = OrderForm

    def form_valid(self, form):
        user = User.objects.first()
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )
    
class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        cache_key = 'products_data_export'
        products_data = cache.get(cache_key)
        if not products_data:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            # elem = products_data[0]
            # name = elem['nme']
            # print('name:', name)
            cache.set(cache_key, products_data, 300)
        return JsonResponse({'products': products_data})
    
    

class OrdersExportView(PermissionRequiredMixin, View):
    permission_required = ['shopapp.export_orders']

    def get(self, request: HttpRequest) -> HttpResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'delivary_address': order.delivary_address,
                'promocode': order.promocode,
                'username': order.user.username,
                'products': [
                    {
                        'name': product.name,
                        'price': product.price
                    }
                    for product in order.products
                ]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})
    

class UserOrdersExportView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = self.kwargs.get('user_id')
        cache_key = f'user_id_{user_id}'
        data = cache.get(cache_key)
        if not data:
            time.sleep(5) # for testing cache
            user = User.objects.filter(id=user_id)
            if not user:
                return JsonResponse({'message': f'Пользователь с id {user_id} не найден.'}, status=400)
            
            orders = Order.objects.filter(user_id=user_id).order_by('pk').prefetch_related('products')
            
            serializer = OrderSerializer(orders, many=True)
            data = serializer.data
            cache.set(cache_key, data, 2 * 60)

        return JsonResponse({'orders': data})

class LatestProductsFeed(Feed):
    title = 'Shop products (latest)'  # Заголовок ленты
    description = 'Updates on changes and addition shop products'  # Подробное описание
    link = reverse_lazy('shopapp:products_list')  #  Ссылка на домашню страницу

    def items(self):
        return Product.objects.filter(archived=False).order_by("-created_at")[:5]
    
    def item_title(self, item: Product):
        return item.name
    
    def item_description(self, item: Product) -> str:
        return item.description[:20]
    
    def item_link(self, item: Product):
        return item.get_absolute_url()

