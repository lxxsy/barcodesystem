from django.urls import path
from . import views


urlpatterns = [
    path('save_formula', views.save_formula),
    path('query_formula<int:num>', views.query_formula),
    path('update_formula', views.update_formula),
]

