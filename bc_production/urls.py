from django.urls import path
from . import views

app_name = 'production'
urlpatterns = [
    path('save_production', views.save_production, name='save_production'),
    path('update_production', views.update_production, name='update_production'),
    path('query_production<int:num>', views.query_production, name='query_production'),
    path('request_data', views.request_data, name='request_data'),
]