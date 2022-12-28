from django.contrib import admin
from .models import (
    Category, 
    Product, 
    ProductImage, 
    Size, 
    Color,
    Campaing,
    Review,
)

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Campaing)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Istifadeci Deyerlendirmesi', {
            "fields": (
                ['customer', 'product', 'star_count', 'created']
            ),
        }),
    )
    readonly_fields = ['customer', 'product', 'star_count', 'created']
    
    
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class ProductImageInline(admin.TabularInline):
    fields = ['image', 'product_image', 'order']
    readonly_fields = ['product_image']
    classes = ['collapse']
    model = ProductImage
    extra = 2
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    fieldsets = (
        ('Kategorya adi ve sekili', {
            "fields": (
                ['supper', 'title', ('image', 'category_image')] 
            ),
        }),
    )
    readonly_fields = ['category_image']
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    fieldsets = (
        ('Ilkin Melumatlar', {
            "fields": ['title', 'slug', ('old_price', 'new_price'), 'category'],
           
        }),  
              
        ('Diger Melumatlar', {
            "fields": ['description', 'content', ('sizes', 'colors'), ('cover', 'product_cover')],
            "classes": ['collapse']
        }),
        (None, {
            "fields": [('updated', 'created'), 'featured'] 
        }),
    )
    
    readonly_fields = ['updated', 'created', 'product_cover', 'slug']
    inlines = [ProductImageInline, ReviewInline]