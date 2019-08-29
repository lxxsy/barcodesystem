from django.urls import path
from . import views


app_name = 'product'
urlpatterns = [
    path('save_product', views.save_product, name='save_product'),
    path('update_product', views.update_product, name='update_product'),
    path('query_product<int:num>', views.query_product, name='query_product'),
    path('quality_trace_back', views.quality_trace_back, name='quality_trace_back'),
]