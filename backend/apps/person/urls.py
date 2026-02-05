from django.urls import path
from .views import (
    AddCallDate,
    GetRegionList,
    GetPrecinctList,
    GetPositionList,
    AddEmployeeCaller,
    GetRegionArmeniaList,
    GetCitiesList,
    GetVillagesList,
    GetProtectedAreasList,
    AddCitizenCaller,
    GetLastEmployee,
    GetLastCitizen,
    AddFireCall,
    GetReserveList
)

urlpatterns = [
    path('addDateCall/', AddCallDate.as_view()),
    path('regions/', GetRegionList.as_view()),
    path('precinct/', GetPrecinctList.as_view()),
    path('position/', GetPositionList.as_view()),
    path('addEmployeeCaller/', AddEmployeeCaller.as_view()),
    path('regionArmenia/', GetRegionArmeniaList.as_view()),
    path('cities/', GetCitiesList.as_view()),
    path('villages/', GetVillagesList.as_view()),
    path('protectedAreasList/', GetProtectedAreasList.as_view()),
    path('reserveList/', GetReserveList.as_view()),
    path('addCitizenCaller/', AddCitizenCaller.as_view()),
    path('getLastEmployee/', GetLastEmployee.as_view()),
    path('getLastCitizen/', GetLastCitizen.as_view()),
    path('addFireCall/', AddFireCall.as_view()),
    
]
