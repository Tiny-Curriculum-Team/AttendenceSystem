from django.urls import path

from . import views

app_name = 'WriteIn'

urlpatterns = [
    path('start/', views.start_record, name='Start Record'),
    path('stop/', views.stop_record, name='Stop Record'),
]
