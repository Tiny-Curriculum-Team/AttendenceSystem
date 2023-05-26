from django.urls import path

from . import views

app_name = 'Analyze'

urlpatterns = [
    path('', views.compute, name='Analyze Data'),
]