from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Order, OrderDetail, Status, Cash, Address, ShipperReceiver, AuctionHistory, Rating
from .serializers import UserSerializers, OrderSerializers, OrderDetailSerializer, CashSerializer,\
    AddressSerializer, StatusSerializer, ShipperReceiverSerializer, ShipperReceiverSerializer2, \
    AutionHistorySerializer, RatingSerializer, OrderStatusSerializer, RatingSerializer2
from .paginators import BasePagination
from django.http import Http404
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers

    parser_classes = (MultiPartParser, FormParser)


    # def get_parsers(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         return []
    #
    #     return super().get_parsers()

    def get_permissions(self):
        if self.action == 'get_current_user':
           return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail= False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=True, url_path="")
    # def get_profile_shipper(self, request, pk):
    #     shipper = User.objects.get(pk=pk)
    #     return Response(UserSerializers(shipper, many=True, context={"request": request}).data,
    #                     status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="ShipperReceiver")
    def get_shipper(self, request, pk):
        shipper = User.objects.get(pk=pk).ShipperReceiver.filter(active=True)

        return Response(ShipperReceiverSerializer2(shipper, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="orders_customer")
    def get_cus(self, request, pk):
        customer = User.objects.get(pk=pk).orders_customer.filter(active=True)

        return Response(OrderStatusSerializer(customer, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="shipper_aution_history")
    def get_shipper_history(self, request, pk):
        shipper = User.objects.get(pk=pk).shipper
        return Response(AutionHistorySerializer(shipper, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="shipper_rating")
    def get_shipper_rating(self, request, pk):
        shipper_rating = User.objects.get(pk=pk).ship.all()

        return Response(RatingSerializer(shipper_rating, many=True, context={"request": request}).data, status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    pagination_class = BasePagination
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializers

    def get_queryset(self):
        order = Order.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            order = Order.filter(order_name__icontains=q)

        order_id = self.request.query_params.get('id')

        if order_id is not None:
            order = order.filter(id=order_id)

        return order

    @action(methods=['get'], detail=True, url_path="get_aution")
    def get_aution(self, request, pk):
        aution = Order.objects.get(pk=pk).order

        return Response(AutionHistorySerializer(aution, many=True).data,
                        status=status.HTTP_200_OK)


class OrderDetailViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    queryset = OrderDetail.objects.filter(active=True)
    serializer_class = OrderDetailSerializer
    parser_classes = (MultiPartParser,)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()


class CashViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Cash
    serializer_class = CashSerializer
        # permission_classes = (permissions.IsAuthenticated,)


class AddressViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class StatusViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @action(methods=['get'], detail=True, url_path="order-status")
    def get_order(self, request, pk):
        order = Status.objects.get(pk=pk).order_status.filter(active=True)

        return Response(OrderStatusSerializer(order, many=True).data, status=status.HTTP_200_OK)


class ShipperReceiverViewSet(viewsets.ModelViewSet):
    serializer_class = ShipperReceiverSerializer
    pagination_class = BasePagination
    queryset = ShipperReceiver.objects.all()


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer2
    queryset = Rating.objects.all()


class AutionViewset(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = AuctionHistory.objects.all()
    serializer_class = AutionHistorySerializer