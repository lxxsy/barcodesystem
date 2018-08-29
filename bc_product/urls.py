from django.urls import path
from . import views


urlpatterns = [
    path('product_save', views.product_save),
    path('product_query<int:num>', views.product_query),
    path('product_update', views.product_update),
]