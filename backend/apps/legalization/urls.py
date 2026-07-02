from django.urls import path
from .views import (
        GetRegionList,
        GetPrecinctList,
        GetLastEmployee,
    )

urlpatterns = [
    path('regions/', GetRegionList.as_view()),
    path('precincts/', GetPrecinctList.as_view()),
    path('getemployee/', GetLastEmployee.as_view()),
]