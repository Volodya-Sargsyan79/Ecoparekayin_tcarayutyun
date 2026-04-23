from django.urls import path
from .views import (MakeCallAPIView)

urlpatterns = [
    path("call/", MakeCallAPIView.as_view())
]