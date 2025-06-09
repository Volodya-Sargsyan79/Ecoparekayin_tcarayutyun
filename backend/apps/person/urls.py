from django.urls import path
from .views import (
    GetPersonList,
    GetPersonPhoneList,
    GetPersonAddressList,
    GetPersonRelativesList,
    GetPersonWorkList
)
    

urlpatterns = [
    path('person/', GetPersonList.as_view()),
    path('person/phone/', GetPersonPhoneList.as_view()),
    path('person/address/', GetPersonAddressList.as_view()),
    path('person/relatives/', GetPersonRelativesList.as_view()),
    path('person/work_list/', GetPersonWorkList.as_view())
]
