from django.urls import path
from . import views

app_name = 'rmaterial'
urlpatterns = [
    path('save_rmaterial', views.save_rmaterial, name='save_rmaterial'),
    path('update_rmaterial', views.update_rmaterial, name='update_rmaterial'),
    path('query_rmaterial<int:num>', views.query_rmaterial, name='query_rmaterial'),
    path('save_gys', views.save_gys, name='save_gys'),
    path('update_gys', views.update_gys, name='update_gys'),
    path('query_gys<int:num>', views.query_gys, name='query_gys'),
    path('save_ylinfo_hgml', views.save_ylinfo_hgml, name='save_ylinfo_hgml'),
    path('update_ylinfo_hgml', views.update_ylinfo_hgml, name='update_ylinfo_hgml'),
    path('query_ylinfo_hgml<int:num>', views.query_ylinfo_hgml, name='query_ylinfo_hgml'),
    path('save_enterstock', views.save_enterstock, name='save_enterstock'),
    path('update_enterstock', views.update_enterstock, name='update_enterstock'),
    path('query_enterstock<int:num>', views.query_enterstock, name='query_enterstock'),
    path('query_stock<int:num>', views.query_stock, name='query_stock'),
]