from django.urls import path
from . import views

app_name = 'formula'
urlpatterns = [
    # 引向配方保存视图
    path('save_formula', views.save_formula, name='save_formula'),
    # 引向配方查询视图
    path('query_formula<int:num>', views.query_formula, name='query_formula'),
    path('update_formula', views.update_formula, name='update_formula'),
]

