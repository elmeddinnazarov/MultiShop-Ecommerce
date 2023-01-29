from django.contrib import admin
from .models import (
    Customer,
    Contact,
    Wishlist,
    BascetItem,
    Order,
    Purchase,
    OrderCoupon,
    Coupon,
    PasswordReset,
    BulkMail
)
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ['user', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['user', 'email', 'first_name', 'last_name', 'phone']

class PurchaseInline(admin.TabularInline):
    model = Purchase
    fields = ['title', 'color', 'size', 'quantity', 'price', 'order', 'product', 'all_price']
    readonly_fields = ['order', 'product']
    extra = 1


class OrderCouponInline(admin.TabularInline):
    model = OrderCoupon
    fields = ['order', 'coupon', 'coupon_code', 'coupon_discount']
    readonly_fields = ['order', 'coupon', 'coupon_code', 'coupon_discount']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ilkin Melumatlar', {
            "fields": (
                ['customer', 'first_name', 'last_name', 'email', 'phone']
            ),
            "classes": ['collapse']
        }),
        ('Adres Melumatlari ', {
            "fields": (
                ['address', 'district', 'city', 'zipcode']
            ),
            "classes": ['collapse']
        }),
        ('Sifaris Melumatlari', {
            "fields": (
                ['total_price', 'total_discount', 'created', 'accepted', 'delivered', 'cancled']
            ),
        }),
    )
    readonly_fields = ['customer', 'first_name', 'last_name', 'email', 'phone', 'address', 'district', 'city', 'zipcode', 'total_price', 'total_discount', 'created']
    inlines = [OrderCouponInline, PurchaseInline]
    
    
    
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    fields = ['code', 'discount_percent', 'expire', 'used_customers']
    readonly_fields = []


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'subject', 'message', 'created']
    readonly_fields = ['created']



@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    fields = ['user', 'expiry', 'uuid', 'token', 'used']
    readonly_fields = ['expiry', 'uuid', 'token']



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    fields = ['customer', 'product', 'created']
    readonly_fields = ['customer', 'product', 'created']

@admin.register(BascetItem)
class BascetItemAdmin(admin.ModelAdmin):
    fields = ['customer', 'product', 'size', 'color', 'quantity', 'created']
    readonly_fields = ['customer', 'created']
    


@admin.register(BulkMail)
class BulkMailAdmin(admin.ModelAdmin):
    fields = ['subject','content','customers','created']
    readonly_fields = ['created']
    








