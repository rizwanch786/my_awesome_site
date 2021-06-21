from django.contrib import admin

# Register your models here.
from .models import Contact, Orders, Product,OrderUpdate
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)