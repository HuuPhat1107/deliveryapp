from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class AutionHistoryAdmin(admin.ModelAdmin):
    search_fields = ['shipper', 'order', 'price']
    list_display = ['id', 'shipper']


class UserAdmin(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    search_fields = ['first_name', 'last_name', 'sex']
    list_display = ['id', 'username', 'sex', 'first_name', 'last_name', 'email', 'is_staff', 'group']


class OrderAdmin(admin.ModelAdmin):

    search_fields = ['order_name', 'note']
    list_filter = ['order_name', 'note', 'customer', 'status']
    list_display = ['order_name', 'note', 'image', 'customer', 'status', 'image_view']
    readonly_fields = ['image_view']

    def image_view(self, Order):
        return mark_safe(
            "<img src='/static/{url}' width='120' />".format(url=Order.image.name)
        )


class CashAdmin(admin.ModelAdmin):
    search_fields = ['user', 'cash']
    list_display = ['user', 'cash']


admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cash, CashAdmin)
admin.site.register(Status)
admin.site.register(AuctionHistory, AutionHistoryAdmin)
