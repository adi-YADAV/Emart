from django.contrib import admin
from ecomapp.models import Product

# Register your models here.
#admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','is_active','cat']
    list_filter=['is_active','cat']
    
admin.site.register(Product,ProductAdmin)