from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import User, Order
from .serializers import UserSerializers, OrderSerializers
from .paginators import BasePagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializers


def index(request):
    return HttpResponse("Delivery App")