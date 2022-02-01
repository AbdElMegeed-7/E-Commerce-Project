from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def home(request, category_slug= None):
  category_page = None
  products = None
  if category_slug != None:
    category_page = get_object_or_404(Category, slug= category_slug)
    products = Product.objects.filter(category=category_page, available=True)
  else:
    products = Product.objects.all().filter(available=True)
    
  context = {
    'category': category_page,
    'products': products,
  }
  return render(request, 'home.html', context)  


def productPage(request, category_slug, product_slug):
  try:
    product = Product.objects.get(category__slug= category_slug, slug= product_slug)
  except Exception as e:
    raise e
  
  context = {
    'product': product,
  }
  return render(request, 'product.html', context) 

def cart(request):
  return render(request, 'cart.html')