from django.contrib import admin

# Register your models here.
from .models import Category, Recommend, Tag, Article, SideBar
# 导入需要管理的数据库表


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'tui',
                    'user', 'views', 'created_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Recommend)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(SideBar)
