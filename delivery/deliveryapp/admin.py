from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', ]


admin.site.register(User)
admin.site.register(Order)
admin.site.register(Shipper)
admin.site.register(Status)
admin.site.register(ShippingMethod)
admin.site.register(Customer)

