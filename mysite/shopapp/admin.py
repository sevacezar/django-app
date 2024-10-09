from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products, save_json_orders
from .models import Product, Order, ProductImage
from .admin_mixins import ExportCSVMixin
from .forms import CSVImportForm, JsonImportForm
# Register your models here.

class OrderInline(admin.TabularInline):
    model = Product.orders.through

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description', 'price'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide',),
        }),
        ('Images', {
            'fields': ('preview', )
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete',
        })
    ]

    def description_short(self, obj: Product) -> str:
        return obj.description if len(obj.description) < 48 else obj.description[:48] + '...'
    
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        
        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )

        self.message_user(request, 'Data from csv was imported')
        return redirect(
            '..'
        )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv',
            ),
        ]
        return new_urls + urls
# admin.site.register(Product, ProductAdmin)



class ProductInline(admin.StackedInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/orders_changelist.html'
    inlines = [
        ProductInline
    ]
    list_display = 'delivary_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username


    def import_json(self, request: HttpRequest) -> HttpResponse:
        """Обычная view-функция"""
        if request.method == 'GET':
            form = JsonImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/json_form.html', context)
        
        form = JsonImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/json_form.html', context, status=400)
        
        save_json_orders(
            file=form.files['json_file'].file,
            encoding=request.encoding,
        )

        self.message_user(request, 'Data from json-file was imported')
        return redirect(
            '..'
        )

    def get_urls(self):
        """Подключение view-функции к urls"""
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-json/',
                self.import_json,
                name='import_orders_json',
            ),
        ]
        return new_urls + urls