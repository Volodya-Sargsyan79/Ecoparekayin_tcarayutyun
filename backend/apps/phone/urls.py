from django.urls import path
from .views import (MakeCallAPIView, upload_call_record, GetCallsList)

urlpatterns = [
    path("call/", MakeCallAPIView.as_view()),
    path('upload_call_record/', upload_call_record, name='upload_call_record'),
    path("call_list/", GetCallsList.as_view()),
]