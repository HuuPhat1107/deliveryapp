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
            user.groups.add(group)

        return user

    avatar = SerializerMethodField()

    def get_avatar(self, user):
        request = self.context['request']
        if user.avatar:
            name = user.avatar.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

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

    def update(self, instance, validated_data):
        fields = instance._meta.fields
        exclude = []
        for field in fields:
            field = field.name.split('.')[-1]
            if field in exclude:
                continue
            exec("instance.%s = validated_data.get(field, instance.%s)" % (field, field))
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = ['id', 'order_name', 'customer',
                  'created_date', 'updated_date', 'status']


class UserPhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']

class OrderDetailSerializer(OrderSerializers):
    # tags = TagSeriazlier(many=True)
    order = OrderSerializers()
    phone_cus = serializers.CharField(source='phone_cus.phone', read_only=True)

    image = SerializerMethodField()

    def get_image(self, order):
        request = self.context['request']
        name = order.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)

    class Meta:
        model = OrderDetail
        fields = ['order', 'description', 'quality', 'image', 'phone_cus', 'note', 'area']