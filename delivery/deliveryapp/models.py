from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    CCCD = models.CharField(max_length=12, unique=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.username

#
# class Category(models.Model):
#     name = models.CharField(max_length=100, null=False, unique=True)
#
#     def __str__(self):
#         return self.name


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cash(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cash = models.CharField(max_length=255, blank=True)


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Don hang
class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="orders_customer")
    status = models.ForeignKey(Status, null=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.order_name


class ShipperReceiver(models.Model):
    order = models.OneToOneField(Order, null=True, on_delete=models.CASCADE)
    shipper = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    price = models.CharField(max_length=255, null=True, blank=True)


class Address(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class OrderDetail(ModelBase):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    quality = models.CharField(max_length=2)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, upload_to='products/%Y/%m')
    phone_cus = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    note = models.TextField(null=True, blank=True)
    area = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# class ActionBase(models.Model):
#     shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ship")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together=('ship')
#         abstract=True
#

class Rating(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ship", null=True)
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name= "customer")
    star = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class AuctionHistory(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipper", null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name="order")
    price = models.TextField(null=True, blank=True)

