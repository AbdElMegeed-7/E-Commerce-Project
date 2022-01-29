from django.shortcuts import render


def home(request):
  return render(request, 'home.html')  

def productPage(request):
  return render(request, 'product.html')