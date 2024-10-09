from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductsListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductArchiveView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,

    ProductsDataExportView,
    OrdersExportView,
    ProductViewSet,
    OrderViewSet,
    UserOrdersListView,
    UserOrdersExportView,
)

app_name = 'shopapp'
routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', (ShopIndexView.as_view()), name='shopapp_refs'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/archive/', ProductArchiveView.as_view(), name='product_archive'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),

    path('products/export/', ProductsDataExportView.as_view(), name='products-export'),
    path('orders/export/', OrdersExportView.as_view(), name='orders-export'),

    path('api/', include(routers.urls)),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders_list'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user_orders_export'),
]
