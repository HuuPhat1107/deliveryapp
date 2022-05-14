from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", views.UserViewSet, 'user')
# router.register("orders", views.OrderViewSet, 'order')
router.register("orderdetail", views.OrderDetailViewSet, 'orderdetail')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]
