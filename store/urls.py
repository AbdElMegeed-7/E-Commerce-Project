from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('<slug:category_slug>/', views.home, name= 'products_by_category'),
  
  # path('about/', views.aboutPage, name='about'),
  path('product/', views.productPage, name='productpage'),
]