from django.urls import path
from . import views


urlpatterns = [
    path('save_rmaterial', views.save_rmaterial),
    path('update_rmaterial', views.update_rmaterial),
    path('query_rmaterial<int:num>', views.query_rmaterial),
    path('save_gys', views.save_gys),
    path('update_gys', views.update_gys),
    path('query_gys<int:num>', views.query_gys),
    path('save_ylinfo_hgml', views.save_ylinfo_hgml),
    path('update_ylinfo_hgml', views.update_ylinfo_hgml),
    path('query_ylinfo_hgml<int:num>', views.query_ylinfo_hgml),
    path('save_enterstock', views.save_enterstock),
    path('update_enterstock', views.update_enterstock),
    path('query_enterstock<int:num>', views.query_enterstock),
    path('query_stock<int:num>', views.query_stock),
]