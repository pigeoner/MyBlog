from os import name
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('', views.reindex, name='reindex'),
    path('index/', views.index, name='index'),
    path('cookie/', views.setCookie, name='setCookie'),
    path('reqtest/', views.reqtest, name='reqtest'),
    path('upload/', views.upload, name='upload'),
    path('dealfile/', views.dealfile, name='dealfile'),
    path('pageinfo/', views.pageinfo, name='pageinfo'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('base/', views.base, name='base'),
]
