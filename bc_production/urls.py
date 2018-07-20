from django.urls import path
from . import views


urlpatterns = [
    path('production_add', views.production_add),
    path('detailed_list', views.detailed_list),
]