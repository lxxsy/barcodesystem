from django.urls import path
from . import views


urlpatterns = [
    path('production_add', views.production_add),
    path('select_product<int:num>', views.select_product),
]