from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class UserSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        groups = validated_data.pop('groups')
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
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

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email', 'avatar'
                  , 'groups']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class TagSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'order_name', 'note',
                  'created_date', 'updated_date', 'active']


class OrderDetailSerializer(OrderSerializers):
    # tags = TagSeriazlier(many=True)
    order = OrderSerializers(read_only=True)

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
        fields = ['order', 'description', 'name',
                                                 'image', 'phone_cus', 'note', 'area']

