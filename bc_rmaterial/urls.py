from django.urls import path
from . import views


urlpatterns = [
    path('save_rmaterial', views.save_rmaterial),
    path('update_rmaterial', views.update_rmaterial),
    path('query_rmaterial<int:num>', views.query_rmaterial),
]