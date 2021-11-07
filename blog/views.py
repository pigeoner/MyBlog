from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from blog.models import Blog
import time

# Create your views here.


def index(request):
    return redirect(reverse('blog:test', args=['chouba']))


def test(request, chouba):
    print(chouba)
    return HttpResponse('test')


def date(request):
    return redirect(reverse('blog:getDate', args={'date': time.strftime("%Y-%m-%d", time.localtime())}))
    # return HttpResponse(time.strftime("%Y-%m-%d", time.localtime()))


def getDate(request, date):
    return HttpResponse(date)


def add_article(request):
    blog = Blog()
    blog.title = '田乾东下楼带饭'
    blog.author = 'cky'
    blog.content = '田乾东和陈可悦相比，那我觉得还是田乾东牛逼'
    blog.save()
    return HttpResponse('change database blogInfo')
