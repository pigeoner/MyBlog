from django import template
import datetime
from blog.models import Article, Tag, Category, SideBar

register = template.Library()

# # use simple tag to show string
# @register.simple_tag
# def total_articles():
#     return Article.objects.filter(status='p').count()

# # use simple tag to set context variable
# @register.simple_tag
# def get_first_article():
#     return Article.objects.filter(status='p').order_by('-pub_date')[0]

# # show rendered template
# @register.inclusion_tag('blog/latest_article_list.html')
# def show_latest_articles(count=5):
#     latest_articles = Article.objects.filter(status='p').order_by('-pub_date')[:count]
#     return {'latest_articles': latest_articles, }


@register.simple_tag
def total_articles():
    return Article.objects.all().order_by('-created_time')


@register.simple_tag
def total_tags():
    return Tag.objects.all()


@register.simple_tag
def total_categories():
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()


@register.simple_tag
def get_new_post():
    # 获取最新文章
    return Article.objects.order_by('-created_time')[:8]


@register.simple_tag
def get_hot_post():
    # 获取热门文章
    return Article.objects.order_by('-views')[:5]


@register.simple_tag
def get_archives():
    # 文章归档
    return Article.objects.dates('created_time', 'month', order='DESC')[:8]


@register.simple_tag
def get_tags():
    # 获取热门文章
    return Tag.objects.all()[:5]
