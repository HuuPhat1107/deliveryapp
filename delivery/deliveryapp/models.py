from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    CCCD = models.CharField(max_length=12, unique=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class ShippingMethod(ModelBase):
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name

# Danh gia
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Don hang
class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    # shipping_method = models.ForeignKey(ShippingMethod,
    #                                     null=True,
    #                                     default=1,
    #                                     on_delete=models.CASCADE,
    #                                     )
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="orders")
    status = models.ForeignKey(Status, null=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.order_name


class Address(models.Model):
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.address


# class OrderDetail(ModelBase):
#     quality = models.CharField(max_length=2)
#     description = models.TextField(null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     image = models.ImageField(null=True, upload_to='products/%Y/%m')
#     phone_cus = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     phone_shipper = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     note = models.TextField()
#     total = models.CharField(max_length=200, blank=True)
#     area = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class ActionBase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipper = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('customer', 'shipper')
        abstract=True


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)
    shipper = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    star = models.CharField(max_length=5, null=False)
    comment = models.TextField()


class AuctionHistory(models.Model):
    shipper = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    price = models.TextField()




