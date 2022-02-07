from locale import currency
from django.shortcuts import get_object_or_404, redirect, render, redirect
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings


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


def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart


def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
            cart_id= _cart_id(request)
            )
    cart.save()
    
  try:  
    cart_item = CartItem.objects.get(cart=cart,product=product)
    if cart_item.quantity < cart_item.product.stock: 
      cart_item.quantity += 1
    cart_item.save()
  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(
                  product= product,
                  quantity= 1,
                  cart=cart
                  )
    cart_item.save()
  
  return redirect('cart_detail')


def cart_detail(request, total= 0, counter= 0, cart_items= None):
  try:
    cart = Cart.objects.get(cart_id= _cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      counter += cart_item.quantity
  except ObjectDoesNotExist:
    pass
  # Stripe
  stripe.api_key = settings.STRIPE_SECRETE_KEY
  stripe_total = int(total * 100)
  description = 'Z-Store - New Order'
  data_key = settings.STRIPE_PUBLISHABLE_KEY
  
  if request.method == 'POST':
    try:
      token = request.POST['stripeToken']
      email = request.POST['stripeEmail']
      billingName = request.POST['stripeBillingName']
      billingAddress = request.POST['stripeBillingAddressLine1']
      billingCity = request.POST['stripeBillingAddressCity']
      billingPostcode = request.POST['stripeBillingAddressZip']
      billingCountry = request.POST['stripeBillingAddressContryCode']
      shippingName = request.POST['stripeShippingName']
      shippingAdress1 = request.POST['stripeShippingAdressLine1']
      shippingCity = request.POST['stripeShippingAdressCity']
      shippingPostcode = request.POST['stripeShippingAdressZip']
      shippingCountry = request.POST['stripeShippingAdressCountryCode'] 
      
      
      customer = stripe.Customer.create(
                email=email,
                source=token,
                )
      charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id, 
                )
      # Creating The Order
      try :
        order_detail = Order.Objects.create(
                       token = token,
                       total = total,
                       emailAddress1 = email,
                       billingCity = billingCity,
                       billingPostcode = billingPostcode,
                       billingCountry = billingCountry,
                       shippingName = shippingName,
                       shippingAdress1 = shippingAdress1,
                       shippingCity = shippingCity,
                       shippingPostcode = shippingPostcode,
                       shippingCountry = shippingCountry,
                      )
        order_detail.save()
        for order_item in cart_items:
          or_item = OrderItem.objects.create(
                       product= order_item.product.name,
                       quantity = order_item.quantity,
                       price = order_item.product.price,
                       order = order_detail,
                      )
          or_item.save()  
          
          #reduce stock
          products= Product.objects.get(id=order_item.product.id)
          products.stock= int(order_item.product.stock - order_item.quantity)
          products.save()
          
          # Print the massege when the order is created
          print("The Order has been Created")
        return redirect('home')
      
      except ObjectDoesNotExist:
        pass                
      
    except stripe.error.CardError as e:
      return False,e
      
  return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description ))


def cart_remove(request, product_id):
  cart= Cart.objects.get(cart_id= _cart_id(request))
  product = get_object_or_404(Product, id= product_id)
  cart_item = CartItem.objects.get(cart=cart, product=product)
  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
  return redirect('cart_detail')

def cart_remove_product(request, product_id):
  cart= Cart.objects.get(cart_id= _cart_id(request))
  product = get_object_or_404(Product, id= product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  cart_item.delete()
  return redirect('cart_detail')