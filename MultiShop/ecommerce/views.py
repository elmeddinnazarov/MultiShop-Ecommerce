from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Avg, F, Count, Max, Min
from .filters import ProductFilter
from django.contrib.postgres.search import TrigramWordSimilarity, SearchQuery, SearchRank, SearchVector
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from .models import (
    Product,
    ProductImage,
    Category,
    Campaing,
    Color,
    Size,
    Review
)


@cache_page(60 * 15)
def home(request):
    
    context = {
    'categories': Category.objects.all()[:12],
    'slide_campaings': Campaing.objects.filter(slide=True),
    'campaings': Campaing.objects.exclude(slide=True),
    'featured_products': Product.objects.filter(featured=True).order_by('?')[:8],
    'recent_products': Product.objects.all().order_by(F('created').desc())[:8],
    }

    return render(request, 'home.html', context=context)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        reviews = product.review_set.all()
        p_images = ProductImage.objects.all()
        all_reviews_count = product.review_set.count
        if self.request.user.is_authenticated:
            customer_review = product.review_set.filter(customer=self.request.user.customer).first()
            reviews = product.review_set.exclude(customer=self.request.user.customer)
        context['reviews'] = reviews
        context['customer_review'] = customer_review
        context['p_images'] = p_images
        context['all_reviews_count'] = all_reviews_count
        return context
  
# def product_detail(request, pk, slug):
#     p_images = ProductImage.objects.all()
#     product = get_object_or_404(Product, pk=pk)
#     reviews = product.review_set.all()
#     customer_review = None
#     if request.user.is_authenticated:
#         customer_review = product.review_set.filter(customer=request.user.customer).first()
#         reviews = product.review_set.exclude(customer=request.user.customer)
        
#     all_reviews_count = product.review_set.count
#     context = {
#         'product': product,
#         'p_images': p_images,
#         'customer_review': customer_review,
#         'reviews': reviews,
#         'all_reviews_count': all_reviews_count
#     }
#     return render(request, 'detail.html', context=context)


class ProductListView(ListView):
    template_name = 'product.html'
    context_object_name = 'products'


    def get_paginate_by(self, *args, **kwargs):
        return int(self.request.GET.get('page_by', 8))

    def get_queryset(self, *args, **kwargs):
        all_products = Product.objects.all()
        sorting = self.request.GET.get('sorting')  
        if search:=self.request.GET.get('search'):
            all_products = all_products.annotate(similarity=TrigramWordSimilarity(search, 'title_az')).filter(similarity__gt=0.3).order_by('-similarity')
            # vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('category__title', weight='C')
            # all_products = all_products.annotate(rank=SearchRank(vector, SearchQuery(search), weights=[0.1, 0.5, 0.7, 0.8])).filter(rank__gte=0.3).order_by('-rank')

        filter_result = ProductFilter(self.request.GET, all_products)
        filtered_products = filter_result.qs
        
        if sorting:
            sorting = F(sorting[1:]).desc(nulls_last=True) if sorting[0] == '-' else F(sorting).asc(nulls_last=True)  
            filtered_products = filtered_products.annotate(avg_review= Avg('review__star_count')).order_by(sorting)
        return filtered_products 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = context['page_obj']
        context['paginator'] = context['page'].paginator
        context['colors'] = Color.objects.all().annotate(count=Count('product'))
        context['sizes'] = Size.objects.all().annotate(count=Count('product'))
        context['price_info'] = Product.objects.all().aggregate(min_value=Min('new_price'), max_value=Max('new_price'))
        return context
    
# def product_list(request):
    
#     currrent_page = request.GET.get('page', 1)
#     sorting = request.GET.get('sorting')  
#     page_by = int(request.GET.get('page_by', 8))
    
#     all_products = Product.objects.all()
    
#     if search:=request.GET.get('search'):
#         all_products = all_products.annotate(similarity=TrigramWordSimilarity(search, 'title_az')).filter(similarity__gt=0.3).order_by('-similarity')
#         # vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('category__title', weight='C')
#         # all_products = all_products.annotate(rank=SearchRank(vector, SearchQuery(search), weights=[0.1, 0.5, 0.7, 0.8])).filter(rank__gte=0.3).order_by('-rank')
    
#     filter_result = ProductFilter(request.GET, all_products)
#     filtered_products = filter_result.qs
#     if sorting:
#         sorting = F(sorting[1:]).desc(nulls_last=True) if sorting[0] == '-' else F(sorting).asc(nulls_last=True)  
#         filtered_products = filtered_products.annotate(avg_review= Avg('review__star_count')).order_by(sorting)
#     paginator = Paginator(filtered_products, page_by)
#     page = paginator.page(currrent_page)
#     products = page.object_list
    
#     context = {
#         'page': page,
#         'paginator': paginator,
#         'products': products,
#         'colors': Color.objects.all().annotate(count=Count('product')),
#         'sizes': Size.objects.all().annotate(count=Count('product')),
#         'price_info': Product.objects.all().aggregate(min_value=Min('new_price'), max_value=Max('new_price'))
        
#     }

    
#     return render(request, 'product.html', context=context)



@login_required
def review(request, pk):
    if request.method == 'GET':
        return redirect(product.get_absolute_url())
    product = get_object_or_404(Product, pk=pk)
    customer = request.user.customer
    form = ReviewForm(request.POST)
    if form.is_valid():
        form.save(customer, product)

    return redirect(product.get_absolute_url())