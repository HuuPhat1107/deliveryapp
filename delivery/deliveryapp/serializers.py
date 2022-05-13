from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class UserSerializers(serializers.ModelSerializer):
    avatar = SerializerMethodField(source='avatar')

    def get_avatar(self, user):
        request = self.context['request']
        name = user.avatar.name
        request = self.context['request']
        if user.avatar and not user.avatar.name.startswith("/static"):
            path = '/static/%s' % user.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class OrderSerializers(ModelSerializer):
    # image = SerializerMethodField()
    #
    # def get_image(self, order):
    #     request = self.context['request']
    #     name = order.image.name
    #     if name.startswith("static/"):
    #         path = '/%s' % name
    #     else:
    #         path = '/static/%s' % name
    #     return request.build_absolute_uri(path)

    class Meta:
        model = Order
        fields = ['id', 'order_name', 'note',
                  'created_date', 'updated_date', 'active']

