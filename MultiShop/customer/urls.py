from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('bascet/', views.bascet, name='bascet'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('confirm-contact/', views.confirm_contact, name='confirm-contact'),
    path('add-to-bascet/<int:pk>/', views.add_to_bascet, name = 'add-to-bascet'),
    path('update-bascet-quantity/<int:pk>/', views.update_bascet_quantity, name = 'update-bascet-quantity'),
    path('remove-bascet/<int:pk>/', views.remove_bascet, name='remove-bascet'),
    path('add-to-wish/<int:pk>/', views.add_to_wish, name = 'add-to-wish'),
    path('remove-wish/<int:pk>/', views.remove_wish, name='remove-wish'),
    path('change-currency/<str:currency>/', views.change_currency, name='change-currency'),
    path('reset-password<str:uuid>/<str:token>', views.reset_password, name='reset-password'),
    path('reset-password-email', views.reset_password_email, name='reset-password-email'),


]
