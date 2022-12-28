from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('confirm-contact/', views.confirm_contact, name='confirm-contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('bascet/', views.bascet, name='bascet'),
    path('remove-bascet/<int:pk>/', views.remove_bascet, name='remove-bascet'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-wish/<int:pk>/', views.remove_wish, name='remove-wish'),
    path('add-to-wish/<int:pk>/', views.add_to_wish, name = 'add-to-wish'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add-to-bascet/<int:pk>/', views.add_to_bascet, name = 'add-to-bascet'),
    path('update-bascet-quantity/<int:pk>/', views.update_bascet_quantity, name = 'update-bascet-quantity'),
]