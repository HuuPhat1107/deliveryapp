from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class UserSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        groups = validated_data.pop('groups')
        user = User(**validated_data)
        user.set_password(user.password)
        create_cash = Cash(user=user)
        user.save()
        create_cash.save()
        for group in groups:
            print(type(group))
            user.groups.add(group)
            if group.name == "shipper":
                user.is_active = False
                user.save()

        return user

    # avatar = SerializerMethodField()

    # def get_avatar(self, user):
    #     request = self.context['request']
    #     if user.avatar:
    #         name = user.avatar.name
    #         if name.startswith("static/"):
    #             path = '/%s' % name
    #         else:
    #             path = '/static/%s' % name
    #
    #         return request.build_absolute_uri(path)

    cash = serializers.CharField(source='cash.cash', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email', 'avatar'
                  , 'groups', 'CCCD', 'sex', 'address', 'phone', 'cash']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'cash': {
                'read_only': True
            }
        }


class OrderSerializers(serializers.ModelSerializer):
    # customer = UserSerializers()
    class Meta:
        model = Order
        fields = ["id", "order_name", "customer", "status"]


class OrderStatusSerializer(serializers.ModelSerializer):
    quality = serializers.IntegerField(source='orderdetail.quality')
    description = serializers.CharField(source='orderdetail.description')
    note = serializers.CharField(source='orderdetail.note')
    image = serializers.ImageField(source='orderdetail.image')
    area = serializers.IntegerField(source='orderdetail.area.id')

    class Meta:
        model = Order
        fields = ['id', 'order_name', 'customer',
                  'created_date', 'updated_date', 'status', 'quality', 'description', 'note', 'image', 'area']

class UserPhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']


class OrderDetailSerializer(OrderSerializers):
    # tags = TagSeriazlier(many=True)
    order = OrderSerializers()
    # phone = serializers.CharField(source='phone_cus.phone', read_only=True)
    phone_cus = UserPhoneSerializers(read_only=True)

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order = Order(**order_data)
        order.save()
        order_detail = OrderDetail(order=order, **validated_data)
        order_detail.phone_cus = order.customer
        order_detail.save()

        return order_detail

    # image = SerializerMethodField()
    #
    # def get_image(self, order):
    #     request = self.context['request']
    #     if order.image:
    #         name = order.image.name
    #         if name.startswith("static/"):
    #             path = '/%s' % name
    #         else:
    #             path = '/static/%s' % name
    #
    #         return request.build_absolute_uri(path)

    class Meta:
        model = OrderDetail
        fields = ['order', 'description', 'image', 'quality', 'phone_cus', 'note', 'area']


class CashSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        cash = validated_data.pop('cash')
        instance.cash = cash + int(instance.cash)
        instance.save()
        return instance

    class Meta:
        model = Cash
        fields = ['cash']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class ShipperReceiverSerializer(serializers.ModelSerializer):
    shipper_first_name = serializers.CharField(source="shipper.first_name", read_only=True)
    shipper_last_name = serializers.CharField(source="shipper.last_name", read_only=True)


    class Meta:
        model = ShipperReceiver
        fields = ["order", 'shipper', 'price', 'shipper_first_name', 'shipper_last_name']


class ShipperReceiverSerializer2(serializers.ModelSerializer):
    shipper_first_name = serializers.CharField(source="shipper.first_name", read_only=True)
    shipper_last_name = serializers.CharField(source="shipper.last_name", read_only=True)

    order = OrderSerializers(read_only=True)

    class Meta:
        model = ShipperReceiver
        fields = ["order", 'shipper', 'price', 'shipper_first_name', 'shipper_last_name']


class AutionHistorySerializer(serializers.ModelSerializer):
    order_name = serializers.CharField(source="order.order_name", read_only=True)
    status = serializers.IntegerField(source='order.status.id', read_only=True)
    shipper_first_name = serializers.CharField(source="shipper.first_name", read_only=True)
    shipper_last_name = serializers.CharField(source="shipper.last_name", read_only=True)
    class Meta:
        model = AuctionHistory
        fields = ['order', 'shipper', 'price', 'order_name', 'shipper_first_name', 'shipper_last_name', 'status']


class RatingSerializer(serializers.ModelSerializer):
    shipper = UserSerializers()
    customer = UserSerializers()

    class Meta:
        model = Rating
        fields = "__all__"

class RatingSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"