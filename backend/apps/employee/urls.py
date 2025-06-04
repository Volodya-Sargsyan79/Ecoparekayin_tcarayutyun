from django.urls import path
from .views import (
    GetPersonList,
    GetPersonRelativesList,
    GetPersonWorkList,
    GetEmployeeFriendsList,
    GetEmployeeRelationList
)
    

urlpatterns = [
    path('person/', GetPersonList.as_view()),
    path('person/relatives/', GetPersonRelativesList.as_view()),
    path('person/work_list/', GetPersonWorkList.as_view()),
    path('person/friends/', GetEmployeeFriendsList.as_view()),
    path('person/relation/', GetEmployeeRelationList.as_view())
]
