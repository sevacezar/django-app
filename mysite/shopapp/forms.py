from django import forms
from django.contrib.auth.models import Group, User
from django.core import validators

from .models import Product, Order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = 'name', 'price', 'description', 'discount'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivary_address', 'promocode', 'user', 'products'

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
    )
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(archived=False),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'
    
    images = MultipleFileField()


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class JsonImportForm(forms.Form):
    json_file = forms.FileField() 