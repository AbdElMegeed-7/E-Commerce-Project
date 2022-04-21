from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug']
  # prepopulated_fields = {'slug', ('name',)}
  
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
  list_display = ['name', 'price', 'stock', 'available', 'created', 'uploaded']
  list_editable = ['price', 'stock','available']
  # prepopulated_fields = {'slug':('name',)}
  list_per_page = 7
  
admin.site.register(Product, ProductAdmin)


class OrderItemAdmin(admin.TabularInline):
  model = OrderItem
  fieldsets = [
    ('Product', {'fields':['product'],}),
    ('Quantity', {'fields':['quantity'],}),
    ('Price', {'fields':['price'],})
  ]
  readonly_fields = ['product', 'quantity', 'price']
  can_delete =False
   
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'email_address', 'created']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'email_address']
    readonly_fields = [
      'id', 'token', 'total', 'email_address', 'created', 'billingName', 
      'billingAddress1', 'billingCity', 'billingPostcode',
      'billingCountry', 'shippingName', 'shippingAddress1',
      'shippingCity', 'shippingPostcode', 'shippingCountry'
    ]
    fieldsets = [
      ('ORDER INFORMATION', {'fields':['id', 'total', 'token', 'created']}),
      ('BILLING INFORMATION', {'fields':['email_address', 'billingName', 
        'billingAddress1', 'billingCity', 'billingPostcode', 'billingCountry',]}),
      ('SHIPPING INFORMATION', {'fields':['shippingName', 'shippingAddress1',
        'shippingCity', 'shippingPostcode', 'shippingCountry']})
    ]
    
    inlines = [ 
               OrderItemAdmin 
              ]
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False