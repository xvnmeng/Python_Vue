"""Python_Vue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.views.generic.base import TemplateView  # 1、增加该行
# 导入接口文件的方法
from  Django_admin.views import add_article, modify_article, get_token
from  Django_admin.views import login, index


urlpatterns = [
    path('admin/', admin.site.urls),
    # 使用通用视图创建最简单的模板控制器，访问 『/』时直接返回 index.html
    path(r'', TemplateView.as_view(template_name="index.html")),
    # 添加文章接口
    path('articles/',add_article),
    path('articles',add_article),
    # 修改文章接口
    # 格式：add_article/17
    path('articles/<int:art_id>',modify_article),
    # 鉴权接口
    path('auth', get_token),
    path('login/', login),
    path('index/', index),
    path('login', login),
    path('index', index),
    path('test', login),
]
