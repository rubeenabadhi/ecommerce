from django.urls import path
from .import views

urlpatterns=[
    path('cartDetails', views.cartDetails, name='cartDetails'),
    path('add/<int:product_id>/', views.add_cart, name='addcart'),
    path('cart_decrement/<int:product_id>/',views.min_cart, name= 'cart_decrement'),
    path('removecart/<int:product_id>/',views.remove_cart,name='removecart'),
    path('checkout',views.checkout,name='checkout'),
    path('payment', views.payments, name='payment'),

    path('success',views.success,name='success')

]