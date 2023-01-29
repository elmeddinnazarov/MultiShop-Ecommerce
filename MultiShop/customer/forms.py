from django import forms
from .models import Customer, Contact, Order, Purchase, OrderCoupon, BascetItem
from django.contrib.auth.models import User
from re import compile
from django.template.defaultfilters import floatformat
from django.core.mail import send_mail
from .models import PasswordReset
from django.conf import settings


phone_compile = compile("^\+994\d{9}$")



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="Username"'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="First Name"'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="Last Name"'}))
    phone = forms.CharField(max_length=13,initial='+994', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="Phone"'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="Email"'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="First Name"'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Pasword Again', 'onfocus': 'this.placeholder = ""', 'onblur': 'this.placeholder="Pasword Again"'}))

    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if username and username.lower() in password.lower():
            raise forms.ValidationError('istifadeci adi sifre olaraq istifade edile bilmez!')
        
        if first_name and last_name and first_name.lower() in password.lower() or last_name.lower() in password.lower():
            raise forms.ValidationError('Adiniz ve soyadiniz sifre olaraq istifade edile bilmez!')        
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Sifreler eyni deyil!')
        
        
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone_compile.search(phone):
            raise forms.ValidationError('Telefon nomresi duzgun yazilmayib!')
        return phone
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu mail adresi movcuddur!')
        return email

    
    def save(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        phone = cleaned_data.get('phone')
        
        new_user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            )

        return new_user 
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control', 'rows': '8'}),
        }
        


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = 'customer', 'accepted', 'delivered', 'cancled', 'total_price', 'total_discount'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Mail Address', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'city': forms.Select(attrs={'placeholder': 'Baki', 'class': 'form-control'}),
            'district': forms.TextInput(attrs={'placeholder': 'Bileceri', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Eli Elizade kuc. Bina:12, Menzil:113', 'class': 'form-control', 'rows': '2'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'AZ10023', 'class': 'form-control'}),
        }
        
    def save(self, customer, coupon, coupon_vaild, total_price, total_price_coupon):
        cleaned_data = self.cleaned_data
        order = Order.objects.create(
            customer = customer,
            first_name = cleaned_data.get('first_name'),
            last_name = cleaned_data.get('last_name'),
            email = cleaned_data.get('email'),
            address = cleaned_data.get('address'),
            phone = cleaned_data.get('phone'),
            city = cleaned_data.get('city'),
            district = cleaned_data.get('district'),
            zipcode = cleaned_data.get('zipcode'),
            total_price = total_price_coupon if coupon_vaild else total_price,
            total_discount = floatformat((total_price - (total_price_coupon if coupon_vaild else total_price)), 3)
        )
        
        if coupon_vaild:
            coupon = OrderCoupon.objects.create(
                order = order,
                coupon = coupon,
                coupon_code = coupon.code,
                coupon_discount = coupon.discount_percent,
            )
            coupon.coupon.used_customers.add(customer)
        
        purchases = []
        bascet = customer.bascetitem_set.all()
        for bi in bascet:
            purchase = Purchase(
                order = order,
                size = bi.size.title,
                color = bi.color.title,
                price = bi.product.new_price,
                quantity = bi.quantity,
                title = bi.product.title,
                product = bi.product,
                all_price = bi.product.new_price * bi.quantity
            )
            
            purchases.append(purchase)
        Purchase.objects.bulk_create(purchases)
        
        bascet.delete()
        return order




class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    
    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        if email and not User.objects.filter(email=email).exists():
            raise forms.ValidationError('İstifadəçi tapılmadı!')
        return email
            
    def send_reset_mail(self, request):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        user = User.objects.get(email=email)
        password_reset = PasswordReset(user=user)
        url = request.build_absolute_uri(password_reset.get_absolute_url())
        # print('get_absolute url', password_reset.get_absolute_url())
        try:
            send_mail(
                'MultiShop Reset Password Validation',
                f'Please go to the link below to reset your MultiShop Account Password.\nLink: {url}',
                settings.EMAIL_HOST_USER,
                [email],
            )
            return True
        except Exception:
            return False

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='New Password Again', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password and password_again and password !=password_again:
            raise forms.ValidationError('Şifrələr eyni deyil!')

    def change_password(self, user):
        password = self.cleaned_data.get('password')
        user.set_password(password )
        
        
