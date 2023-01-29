from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from secrets import token_urlsafe
from datetime import timedelta
from django.utils import timezone
from uuid import uuid4
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    
    def __str__(self):
        return self.user.get_full_name()
    
    class Meta:
        verbose_name = "İstifadəçi"
        verbose_name_plural = "İstifadəçilər"
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def username(self):
        return self.user.username
    
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "İsmarıc"
        verbose_name_plural = "İsmarıclar"

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.customer} - {self.product}'

    class Meta:
        verbose_name = "Favorit"
        verbose_name_plural = "Favorit lər"
        
class BascetItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE)
    size = models.ForeignKey('ecommerce.Size', on_delete=models.CASCADE)
    color = models.ForeignKey('ecommerce.Color', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer} - {self.product}- {self.size}- {self.color} - {self.quantity}'
    
    
    class Meta:
        verbose_name = "Səbəttəki Məhsul"
        verbose_name_plural = "Səbət"
        ordering = ['-created']
       
       
class Coupon(models.Model):
    code = models.CharField(max_length=20)
    discount_percent = models.FloatField()
    expire = models.DateField()
    used_customers = models.ManyToManyField(Customer, blank=True, related_name='used_coupons')
    
    def is_valid(self, customer):
        return self.expire > timezone.localdate() and not customer in  self.used_customers.all()
    
    def __str__(self):
        return self.code#, self.discount_percent, self.expire
    
    class Meta:
        verbose_name = "Kupon"
        verbose_name_plural = "Kuponlar"
        
CITY_CHOICES = [
    ('baku', 'Baki'),
    ('kurdamir', 'Kurdamir'),
    ('samakhi', 'Samaxi'),
]
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    city = models.CharField(choices=CITY_CHOICES, max_length=50)
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    cancled = models.BooleanField(default=False)
    total_price = models.FloatField()
    total_discount = models.FloatField()
    

    
    
    def __str__(self):
        return f'{self.customer}'
    
    class Meta:
        verbose_name = "Sifariş"
        verbose_name_plural = "Sifarişlər"


class OrderCoupon(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='coupon')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    coupon_code = models.CharField(max_length=20, null=True, blank=True)
    coupon_discount = models.FloatField(max_length=20, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.coupon.code#, self.coupon_code, self.coupon_discount
    
    class Meta:
        verbose_name = "Istifade Edilen Kupon"
        verbose_name_plural = "Istifade Edilen Kuponlar"
    

class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    size =  models.CharField(max_length=100)
    color =  models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    title = models.CharField(max_length=100)
    product = models.ForeignKey('ecommerce.Product', on_delete=models.SET_NULL, null=True)
    all_price = models.FloatField ()


    def __str__(self):
        return self.title#, self.quantity, self.color, self.size
    
    class Meta:
        verbose_name = "Satin Alinan"
        verbose_name_plural = "Satin Alinanlar"
        
        
        
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid4)
    token = models.TextField(null=True, blank=True)
    used = models.BooleanField(default=False)

    
    def save(self, *args, **kwargs):
        self.expiry = timezone.localdate() + timedelta(days=1)
        self.token = token_urlsafe(100)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used and self.expiry > timezone.localdate()
       
    def get_absolute_url(self):
        # print('TOKEN BURDA', self.token)
        thisurl =  reverse('customer:reset-password', kwargs= {'uuid': self.uuid, 'token': self.token})
        return thisurl
        
    
    def __str__(self):
        return self.user.get_full_name()


class BulkMail(models.Model):
     subject = models.CharField(max_length=100)
     content = models.TextField()
     customers = models.ManyToManyField(Customer)
     created = models.DateField(auto_now_add=True)