from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('', views.index, name='index'),
    path('test/<str:chouba>/', views.test, name='test'),
    path('date/', views.date, name='date'),
    re_path(r'date/(?P<date>\d{4}-\d{2}-\d{2})/',
            views.getDate, name='getDate')
]
