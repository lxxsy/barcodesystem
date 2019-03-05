from django.urls import path
from . import views


urlpatterns = [
    path('save_product', views.save_product),
    path('update_product', views.update_product),
    path('query_product<int:num>', views.query_product),
    path('a', views.a),
]