from django.urls import path
from .views import (
    GetEmployeeList,
    GetEmployeeRelativesList,
    GetEmployeePalsList,
    GetEmployeeFriendsList,
    GetEmployeeRelationList
)
    

urlpatterns = [
    path('employee/', GetEmployeeList.as_view()),
    path('employee/relatives/', GetEmployeeRelativesList.as_view()),
    path('employee/pals/', GetEmployeePalsList.as_view()),
    path('employee/friends/', GetEmployeeFriendsList.as_view()),
    path('employee/relation/', GetEmployeeRelationList.as_view())
]
