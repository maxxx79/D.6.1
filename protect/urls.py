from django.urls import path
from .views import IndexView, AppointmentView

urlpatterns = [
    path('', IndexView.as_view(), name='start'),
    path('1/', AppointmentView.as_view(), name='start2'),
        ]

