from django.urls import path
from .views import (
    GetPersonList,
    GetPersonRelativesList,
    GetPersonWorkList
)
    

urlpatterns = [
    path('person/', GetPersonList.as_view()),
    path('person/relatives/', GetPersonRelativesList.as_view()),
    path('person/work_list/', GetPersonWorkList.as_view())
]
