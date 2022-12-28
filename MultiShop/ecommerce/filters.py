import django_filters as filters
from .models import Product, Category, Size, Color



class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='new_price', lookup_expr='gt')
    max_price = filters.NumberFilter(field_name='new_price', lookup_expr='lt')
    size = filters.ModelMultipleChoiceFilter(field_name='sizes__title',to_field_name='title', queryset=Size.objects.all())
    
    class Meta:
        model = Product
        fields = ['category']