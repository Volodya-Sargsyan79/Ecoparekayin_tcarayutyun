from django.urls import path
from .views import (
    GetPersonList,
    GetPersonPhoneList,
    GetPersonAddressList,
    GetPersonCarList,
    GetPersonRelativesList,
    GetPersonStudyList,
    GetPersonSoldierList,
    GetPersonWorkList
)
    

urlpatterns = [
    path('person/', GetPersonList.as_view()),
    path('person/phone/', GetPersonPhoneList.as_view()),
    path('person/address/', GetPersonAddressList.as_view()),
    path('person/car/', GetPersonCarList.as_view()),
    path('person/relatives/', GetPersonRelativesList.as_view()),
    path('person/study/', GetPersonStudyList.as_view()),
    path('person/soldier/', GetPersonSoldierList.as_view()),
    path('person/work/', GetPersonWorkList.as_view())
]
