from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  # path('about/', views.aboutPage, name='about'),
  path('product/', views.productPage, name='productpage'),
]