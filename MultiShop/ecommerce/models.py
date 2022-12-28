from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.admin import display
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from imagekit.models.fields import ProcessedImageField
from .utils import convert_slug
# Create your models here.



class Category(models.Model):
    supper = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Kategorya Adi')
    image = models.ImageField(upload_to='category-images/', null=True)
    created = (models.DateTimeField(auto_now_add=True))
    
    class Meta:
        verbose_name = "Kategorya"
        verbose_name_plural = "Kategoryalar"

    def __str__(self):
        return self.title
    
    def is_super(self):
        return self.category_set.exists()
    
    
    @display(description='Kateqorya sekili')
    def category_image(self):
        return format_html(f'<img width=250 src="{self.image.url}">')
    
 
class Campaing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    discount = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True)
    image = models.ImageField(upload_to='campaing_images/')
    created = models.DateField(auto_now_add=True)
    slide = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kampanya"
        verbose_name_plural = "Kampanyalar"
    
class Size (models.Model):
    title = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Ölçü"
        verbose_name_plural = "Ölçülər"
    
class Color (models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Rəng"
        verbose_name_plural = "Rənglər"
        
class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlıq')
    slug = models.SlugField(null=True, blank=True)
    description = RichTextField(max_length=200, verbose_name='Məzmun')
    content = RichTextField(verbose_name='Haqqinda')
    old_price = models.FloatField(validators=[MinValueValidator(0.1)] , verbose_name='Kohne Qiymet')
    new_price = models.FloatField(validators=[MinValueValidator(0.1)] , verbose_name='Hazirki Qiymet')
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kateqorya')
    cover = ProcessedImageField(upload_to='products/product-cover-images/', format='JPEG', options={'quality': 60}, verbose_name='Qapaq Sekili')
    campaings = models.ManyToManyField(Campaing, related_name='products')
    featured = models.BooleanField(default=False)
    updated = models.DateField(auto_now=True, verbose_name='Yenilənmə Tarixi')
    created = models.DateField(auto_now_add=True, verbose_name='Yerləşdirilmə Tarixi')
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"


    @display(description='Qapaq Sekili')
    def product_cover(self):
        return format_html(f'<img width=250 src="{self.cover.url}">')

    def get_absolute_url(self):
        return reverse("ecommerce:product-detail", kwargs={"pk": self.pk, "slug": self.slug})

 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = convert_slug(self.title)
        super().save(*args, **kwargs)



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='products/product-images/', format='JPEG', options={'quality': 60})
    order = models.IntegerField(validators=[MinValueValidator(1)])

    @display(description='Mehsulun Movcud Sekilleri')
    def product_image(self):
        return format_html(f'<img width=250 src="{self.image.url}">')
    
    class Meta:
        ordering = ['order']
        verbose_name = "Məhsul Şəkili"
        verbose_name_plural = "Məhsul Şəkililləri"
    

class Review(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)