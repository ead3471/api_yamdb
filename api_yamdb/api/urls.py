from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, AuthViewSet


router_api_v1 = DefaultRouter()
router_api_v1.register(r'^users', UserViewSet)
router_api_v1.register(r'^auth', AuthViewSet)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
