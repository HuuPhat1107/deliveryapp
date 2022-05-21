from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", views.UserViewSet, 'user')
# router.register("orders", views.OrderViewSet, 'order')
router.register("orderdetail", views.OrderDetailViewSet, 'orderdetail')
router.register("order", views.OrderViewSet, "order")
router.register("cash", views.CashViewSet, "cash")
router.register("address", views.AddressViewSet, "address")
router.register("status", views.StatusViewSet, "status")
# router.register("shipperreceivers", views.ShipperReceiverViewSet, "shipperreceiver")
router.register("rating", views.RatingViewSet, "rating")
router.register("aution", views.AutionViewset, "aution")
router.register("receive", views.ShipperReceiverViewSet, "receive")

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]
