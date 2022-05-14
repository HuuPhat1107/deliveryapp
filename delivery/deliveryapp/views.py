from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import User, Order, OrderDetail, Tag
from .serializers import UserSerializers, OrderSerializers, OrderDetailSerializer
from .paginators import BasePagination
from django.http import Http404
from django.conf import settings


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers

    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'get_current_user':
           return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail= False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

#
# class OrderViewSet(viewsets.ModelViewSet, generics.ListAPIView, generics.RetrieveAPIView):
#     # queryset = Order.objects.filter(active=True)
#     # serializer_class = OrderSerializers
#     # pagination_class = BasePagination
#     #
#     # def get_queryset(self):
#     #     order = Order.objects.filter(active=True)
#     #
#     #     q = self.request.query_params.get('q')
#     #     if q is not None:
#     #         order = Order.filter(subject__icontains=q)
#     #
#     #     order_id = self.request.query_params.get('product')
#     #
#     #     if order_id is not None:
#     #         order = order.filter(product=order_id)
#     #
#     #     return order
#     queryset = Order.objects.filter(active=True)
#     serializer_class = OrderSerializers
#
#     @action(methods=['post'], detail=True, url_path="tags")
#     def add_tag(self, request, pk):
#         try:
#             order = self.get_object()
#         except Http404:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             tags = request.data.get("tags")
#             if tags is not None:
#                 for tag in tags:
#                     t, _ = Tag.objects.get_or_create(name=tag)
#                     order.tags.add(t)
#
#                 order.save()
#
#                 return Response(self.serializer_class(order).data,
#                                 status=status.HTTP_201_CREATED)
#
#         return Response(status=status.HTTP_404_NOT_FOUND)


class OrderDetailViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    queryset = OrderDetail.objects.filter(active=True)
    serializer_class = OrderDetailSerializer


def index(request):
    return HttpResponse("Delivery App")