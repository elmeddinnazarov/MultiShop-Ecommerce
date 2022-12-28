from django.shortcuts import render, redirect, get_object_or_404
from.forms import RegisterForm, ContactForm, CheckoutForm
from django.contrib.auth import login, logout, authenticate
from .models import (
    Contact, Customer, Wishlist, BascetItem, Order, Coupon )
from ecommerce.models import Product
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
# Create your views here.



def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:home')
    return render(request, 'contact.html', context={'form': form})

def confirm_contact(request):
    if request.method == 'GET':
        return redirect('customer:contact')
    elif request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        return redirect('customer:contact')
    
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
         username = request.POST.get('username')
         password  = request.POST.get('password')
         user = authenticate(username=username, password=password)
         if user:
             login(request, user)
             nextUrl = request.GET.get('next')
             return redirect(nextUrl or 'ecommerce:home')
         else:
            return render(request, 'login.html', context={'unsuccess': True })
            
def logout_view(request):
    logout(request)
    return redirect('customer:login') 

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', context={'form': form})

    elif request.method == 'POST':
        form = RegisterForm(data=request.POST)
        accepted = request.POST.get('accepted')
        if form.is_valid() and accepted:
            customer = form.save()
            login(request, customer.user)
            return redirect('ecommerce:home')
        elif not accepted:
            return render(request, 'register.html', context={'form': form, 'not_accepted': True})
        else:
            return render(request, 'register.html', context={'form': form})
            
def profile(request):
    if request.method == 'GET':
        form = RegisterForm(data=request.POST)
        return render(request, 'profile.html', context={'form': form})
    elif request.method == 'POST':
        pass
            
  
  
@login_required
def wishlist(request):
    customer = request.user.customer
    wishlist = customer.wishlist_set.all()
    return render(request, 'wishlist.html', context={'wishlist': wishlist})
      
@login_required
def add_to_wish(requset, pk):

    customer = requset.user.customer
    product = Product.objects.get(pk=pk)
    current_wish = Wishlist.objects.filter(customer=customer,product=product)
    if current_wish:
        current_wish.delete()
    else:
        Wishlist.objects.create(customer=customer, product=product)
    next_url = requset.GET.get('next')
    return redirect(next_url)

@login_required
def remove_wish(request, pk):
    wish = get_object_or_404(Wishlist, pk=pk)
    wish.delete()
    return redirect('customer:wishlist')


@login_required
def bascet(request):
    coupon_code = request.GET.get('coupon_code')
    coupon = Coupon.objects.filter(code=coupon_code).first()
    customer = request.user.customer
    bascet = customer.bascetitem_set.all()
    bascet = bascet.annotate(total_price=F('product__new_price') * F('quantity'))
    total_bascet_price = bascet.aggregate(total_bascet_price=Sum('total_price')).get('total_bascet_price') or 0
    if total_bascet_price == 0:
        shipping_price =0
    elif total_bascet_price <= 30:
        shipping_price = 5
    elif 30 < total_bascet_price <= 120:
        shipping_price = total_bascet_price * 0.165
    else:
        shipping_price = 20
    old_shipping_price = shipping_price
    shipping_free = False
    if total_bascet_price >= 200:
        shipping_free = True
        shipping_price = 0
    total_price = total_bascet_price + shipping_price
    coupon_discount = None
    total_price_with_coupon = None
    if coupon:
        coupon_discount = total_bascet_price * coupon.discount_percent / 100
        total_price_with_coupon = total_price - coupon_discount
        
    context = {
        'bascet': bascet,
        'total_bascet_price': total_bascet_price,
        'coupon': coupon,
        'coupon_discount': coupon_discount,
        'total_price_with_coupon': total_price_with_coupon,
        'invalid_coupon': bool(coupon_code and (not coupon or not coupon.is_valid(customer))),
        'coupon_code': coupon_code,
        'coupon_is_vaild': coupon and coupon.is_valid(customer),
        'shipping_price': shipping_price,
        'shipping_free': shipping_free,
        'total_price': total_price,
        'old_shipping_price': old_shipping_price
        # coupon_code false olsa kupon invaliddir, True olsa: bu adda kupon varsa sistemde coupon True olur ve not coupon = False olur. not coupon False olsa invalid coupon False olur ve kpon do
    }    
    
    return render(request, 'bascet.html', context=context)

@login_required
def add_to_bascet(request,pk):
    if request.method == 'POST':
        customer = request.user.customer
        product = get_object_or_404(Product, pk=pk)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        BascetItem.objects.create(
            customer=customer, product=product, size_id=size, color_id=color, quantity=quantity
        )
        nexturl = request.POST.get('next')
        return redirect(nexturl or 'customer:bascet')
    else:
        return redirect('ecommerce:home')

@login_required
def remove_bascet(request, pk):
    bascetitem = get_object_or_404(BascetItem, pk=pk)
    bascetitem.delete()
    return redirect('customer:bascet')

@login_required
def update_bascet_quantity(request, pk):
    quantity = request.POST.get('quantity')
    bascet = get_object_or_404(BascetItem, pk=pk)
    bascet.quantity = quantity
    bascet.save()
    return redirect('customer:bascet')


def checkout(request):
    user = request.user
    coupon_code = request.GET.get('coupon_code')
    coupon = Coupon.objects.filter(code=coupon_code).first()
    customer = request.user.customer
    bascet = customer.bascetitem_set.all()
    bascet = bascet.annotate(total_price=F('product__new_price') * F('quantity'))
    total_bascet_price = bascet.aggregate(total_bascet_price=Sum('total_price')).get('total_bascet_price') or 0
    if total_bascet_price == 0:
        shipping_price =0
    elif total_bascet_price <= 30:
        shipping_price = 5
    elif 30 < total_bascet_price <= 120:
        shipping_price = total_bascet_price * 0.165
    else:
        shipping_price = 20
    old_shipping_price = shipping_price
    shipping_free = False
    if total_bascet_price >= 200:
        shipping_free = True
        shipping_price = 0
    total_price = total_bascet_price + shipping_price
    coupon_discount = None
    total_price_with_coupon = None
    if coupon:
        coupon_discount = total_bascet_price * coupon.discount_percent / 100
        total_price_with_coupon = total_price - coupon_discount

    coupon_is_valid = coupon and coupon.is_valid(customer)
        
    form = CheckoutForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    saved_money = float(old_shipping_price) + float(coupon_discount if coupon_discount != None else 0)
    context = {
    'form': form,
    'bascet': bascet,
    'coupon_code': coupon_code,
    'total_price': total_price,
    'total_bascet_price': total_bascet_price,
    'shipping_price': shipping_price,
    'total_price_with_coupon': total_price_with_coupon,
    'coupon_discount': coupon_discount,
    'old_shipping_price': old_shipping_price,
    'saved_money': saved_money,
    }
    if request.method == 'GET':
        return render(request, 'checkout.html', context=context)
    elif request.method == 'POST':
        form = CheckoutForm(data=request.POST)
        if form.is_valid():
            order = form.save(request.user.customer, coupon, coupon_is_valid, total_price, total_price_with_coupon)
            return redirect('ecommerce:home')
        # email = request.POST.get('email')
        # phone = request.POST.get('phone')
        # last_name = request.POST.get('last_name')
        # first_name = request.POST.get('first_name')
        # address = request.POST.get('address')
        # district = request.POST.get('district')
        # city = request.POST.get('city')
        # zipcode = request.POST.get('zipcode')
        # checkout = CheckoutForm(first_name=first_name, email=email, last_name=last_name, phone=phone, address=address, district=district, city=city, zipcode=zipcode)
        # checkout.save()
        # return redirect('customer:basket')
        
        
        



