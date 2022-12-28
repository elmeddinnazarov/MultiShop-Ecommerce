from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Avg, F
from .filters import ProductFilter
from .models import (
    Product,
    ProductImage,
    Category,
    Campaing,
)


# Create your views here.
def home(request):
    
    context = {
    'categories': Category.objects.all()[:12],
    'slide_campaings': Campaing.objects.filter(slide=True),
    'campaings': Campaing.objects.exclude(slide=True),
    'featured_products': Product.objects.filter(featured=True).order_by('?')[:8],
    'recent_products': Product.objects.all().order_by(F('created').desc())[:8],
    }

    return render(request, 'home.html', context=context)


def product_detail(request, pk, slug):
    product = Product.objects.get(pk=pk)
    p_images = ProductImage.objects.all()
    return render(request, 'detail.html', context={'product': product, 'p_images': p_images})


def product_list(request):
    
    currrent_page = request.GET.get('page', 1)
    sorting = request.GET.get('sorting', '-created')  
    sorting = F(sorting[1:]).desc(nulls_last=True) if sorting[0] == '-' else F(sorting).asc(nulls_last=True)  
    page_by = int(request.GET.get('page_by', 8))
    
    all_products = Product.objects.all()
    filter_result = ProductFilter(request.GET, all_products)
    filtered_products = filter_result.qs
    filtered_products = filtered_products.annotate(avg_review= Avg('review__star_count')).order_by(sorting)
    paginator = Paginator(filtered_products, page_by)
    page = paginator.page(currrent_page)
    products = page.object_list
    
    context = {
        'page': page,
        'paginator': paginator,
        'products': products
    }

    
    return render(request, 'product.html', context=context)
