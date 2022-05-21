from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    CCCD = models.CharField(max_length=12, null=True)
    phone = models.CharField(max_length=10, null=True)
    sex = models.CharField(max_length=10, default="Nam")
    address = models.CharField(max_length=255, null=True)

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
    cash = models.IntegerField(default=0)

    def __str__(self):
        return str(self.cash)


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Don hang
class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    customer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL, related_name="orders_customer")
    status = models.ForeignKey(Status, null=True, default=1, on_delete=models.SET_NULL, related_name="order_status")

    def __str__(self):
        return self.order_name


class ShipperReceiver(ModelBase):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 primary_key=True, related_name="ShipperR")
    shipper = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="ShipperReceiver")
    price = models.IntegerField(default=0)


class Address(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class OrderDetail(ModelBase):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, related_name="orderdetail")
    quality = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='orders/%Y/%m')
    phone_cus = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    note = models.TextField(null=True, blank=True)
    area = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order.order_name


# class ActionBase(models.Model):
#     shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ship")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together=('ship')
#         abstract=True

# class ActionBase(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cus")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         # unique_together=('cus')
#         abstract=True
#
#
# class Action(ActionBase):
#     LIKE, HAHA, HEART = range(3)
#     ACTIONS = [
#         (LIKE, 'like'),
#         (HAHA, 'haha'),
#         (HEART, 'heart')
#     ]
#     type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ship")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    star = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class AuctionHistory(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipper", null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name="order")
    price = models.IntegerField(default=0)


class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)