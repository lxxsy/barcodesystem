"""BarcodeSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 使用xadmin后台，不使用系统自带的admin
    path('admin/', xadmin.site.urls),
    path('product/', include('bc_product.urls', namespace='product')),
    path('production/', include('bc_production.urls', namespace='production')),
    path('rmaterial/', include('bc_rmaterial.urls', namespace='rmaterial')),
    path('formula/', include('bc_formula.urls', namespace='formula')),
]




