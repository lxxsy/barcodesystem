from django.urls import path
from . import views


urlpatterns = [
    # path('production_save1', views.production_save1),
    path('select_product<int:num>', views.select_product),
    path('production_save', views.production_save),
    path('update_production', views.update_production),
    path('add_production', views.add_production),
    path('a', views.a),
]