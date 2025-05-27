from django.urls import path
from .views import (
    GetRecommendatuinEmployee
)
    

urlpatterns = [
    path('employee/', GetRecommendatuinEmployee.as_view())
]
