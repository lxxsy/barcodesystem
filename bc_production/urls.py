from django.urls import path
from . import views


urlpatterns = [
    path('production_save', views.production_save),
    path('select_product<int:num>', views.select_product),
    # path('a', views.a),
    path('file', views.file),
    path('update_production', views.update_production),
    path('add_production', views.add_production),
]