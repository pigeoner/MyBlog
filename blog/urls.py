from os import name
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    # path('', views.reindex, name='reindex'),
    path('', views.index, name='index'),
    path('album/',views.album, name='album'),
    path('album/<int:id>',views.albums, name='albums'),
    path('picture/<int:id>',views.picture,name='picture'),
    path('tool/',views.tool, name='tool'),
    path('tools/<int:id>',views.tools, name='tools'),
    path('about/', views.about, name='about'),
    path('edit/', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('deleteArticle/', views.deleteArticle, name='deleteArticle'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('tag/<str:tag>/',views.tag,name='tag'),
    path('category/<str:category>/', views.category, name='category'),
    path('base_category/', views.base_category, name='base_category'),
    path('userlogin/', views.userLogin, name='userlogin'),
    path('userlogout/', views.userLogout, name='userlogout'),
    path('praise/', views.praise, name='praise'),
    path('star/', views.star, name='star'),
    path('space/', views.space, name='space'),
]
