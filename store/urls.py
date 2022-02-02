from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('category/<slug:category_slug>/', views.home, name= 'products_by_category'),
  # path('about/', views.aboutPage, name='about'),
  path('category/<slug:category_slug>/<slug:product_slug>/', views.productPage, name='product_detail'),
  path('cart/', views.cart_detail, name="cart_detail"),
  path('cart/add/<int:product_id>/', views.add_cart, name="add_cart"),
]