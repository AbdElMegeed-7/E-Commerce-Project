from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('<slug:category_slug>/', views.home, name= 'products_by_category'),
  
  # path('about/', views.aboutPage, name='about'),
  path('<slug:category_slug>/<slug:product_slug>/', views.productPage, name='product_detail'),
]