from django.urls import path
from .import views
urlpatterns=[
    path('',views.home,name='home'),
    path('search', views.searching, name='search'),

    path('<slug:c_slug>/s',views.home,name='categview'),
    path('<slug:c_slug>/<slug:product_slug>', views.detail,name='detail'),
    path('about', views.about, name='about'),
    path('contact',views.contact,name='contact'),

    ]
