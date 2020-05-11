from django.urls import include
from rest_framework import routers
from rest_framework.urls import url
from .views import MessageViewSet

router = routers.DefaultRouter()
router.register("messages", MessageViewSet)

urlpatterns = [
    url("", include(router.urls)),
]
