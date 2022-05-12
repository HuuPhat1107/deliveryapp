from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import User
from  .serializers import UserSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers


def index(request):
    return HttpResponse("Delivery App")