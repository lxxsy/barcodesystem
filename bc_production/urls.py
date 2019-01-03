from django.urls import path
from . import views


urlpatterns = [
    # path('production_save1', views.production_save1),
    path('save_production', views.save_production),
    path('update_production', views.update_production),
    path('query_production<int:num>', views.query_production),
    path('add_production', views.add_production),
    path('a', views.a),
]