from django.urls import path
from .views import (
    GetRegionList,
    GetPrecinctList,
    GetPositionList,
    AddEmployee,
    GetLastEmployee,
    GetLastCar,
    GetLastRoute,
    GetStationShiftList,
    AddStationShift,
    GetStationShift,
    AddRoute,
    GetEmployee,
    GetRouteMap
)

urlpatterns = [
    path('regions/', GetRegionList.as_view()),
    path('precinct/', GetPrecinctList.as_view()),
    path('position/', GetPositionList.as_view()),
    path('addEmployee/', AddEmployee.as_view()),
    path('getlastemployee/', GetLastEmployee.as_view()),
    path('getemployee/<int:pk>/', GetEmployee.as_view()),
    path('getlastcar/', GetLastCar.as_view()),
    path('getlastroute/', GetLastRoute.as_view()),
    path('getstationshiftlist/', GetStationShiftList.as_view()),
    path('getstationshift/<int:pk>/', GetStationShift.as_view()),
    path('addstationshift/', AddStationShift.as_view()),
    path('addroute/', AddRoute.as_view()),
    path('routes/<int:pk>/', GetRouteMap.as_view()),
]
