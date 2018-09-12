from django.urls import path
from . import views


urlpatterns = [
    path('save_rmaterial', views.save_rmaterial),
]