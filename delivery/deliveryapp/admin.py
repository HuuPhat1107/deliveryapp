from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import *


class AutionHistoryAdmin(admin.ModelAdmin):
    list_filter = ['shipper', 'order', 'price']
    search_fields = ['shipper', 'order', 'price']
    list_display = ['id', 'shipper']


class CusUser(UserAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    'sex',
                    'CCCD',
                    'avatar',
                    'phone',
                    'address',
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ['first_name', 'last_name', 'sex', 'is_active']
    list_display = ['id', 'username', 'sex', 'CCCD', 'first_name', 'last_name', 'email', 'is_staff', 'group', "is_active"]


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_name']
    list_filter = ['order_name', 'customer', 'status']
    list_display = ['order_name', 'customer', 'status']
    # readonly_fields = ['image_view']

    # def image_view(self, Order):
    #     return mark_safe(
    #         "<img src='/static/{url}' width='120' />".format(url=Order.image.name)
    #     )


class RatingAdmin(admin.ModelAdmin):
    search_fields = ['id', 'shipper', 'customer', 'created_date', 'updated_date']
    list_filter = ['shipper', 'customer']
    list_display = ['id', 'shipper', 'customer', 'star', 'created_date']


class CashAdmin(admin.ModelAdmin):
    search_fields = ['user', 'cash']
    list_display = ['user', 'cash']


admin.site.register(User, CusUser)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(Cash, CashAdmin)
admin.site.register(Status)
admin.site.register(Rating, RatingAdmin)
admin.site.register(AuctionHistory, AutionHistoryAdmin)
admin.site.register(Address)
admin.site.register(ShipperReceiver)