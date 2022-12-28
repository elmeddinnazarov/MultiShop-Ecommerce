from django.template import Library
from ecommerce.models import Category
from django.db.models import Count
from customer.models import Wishlist
register = Library()


@register.inclusion_tag(filename='inclusions/categories.html')
def categories():
    return {'categories': Category.objects.all().annotate(category_count=Count('category')).order_by('-category_count')}


@register.filter
def is_wished(product, request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(product=product, customer=request.user.customer).exists()
    return False


@register.simple_tag
def user_product_info(request):
    if not request.user.is_authenticated:
        return {}
    customer = request.user.customer
    bascet_count = customer.bascetitem_set.count()
    wishlist_count = customer.wishlist_set.count()
    return {'bascet_count': bascet_count, 'wishlist_count': wishlist_count}