from django.urls import path

from . import views

app_name = 'slider'
urlpatterns = [
    path('demo', views.demo, name='demo'),
]
