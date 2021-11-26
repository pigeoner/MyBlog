from django.http import response
from django.http.response import Http404
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import time
import os

from blog.models import Article

# Create your views here.


def reindex(request):
    return redirect(reverse('blog:index'))
    # return redirect(reverse('blog:base'))


def index(request):
    # return redirect(reverse('blog:test', args=['chouba']))
    article = Article.objects.all().order_by('-created_time')
    try:
        dlist = []
        paginator = Paginator(dlist, 6)
        page_num = request.GET.get('page', default='1')
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e:
            page_num = 1
            page = paginator.page(page_num)
        except EmptyPage as e:
            if int(page_num) > paginator.num_pages:
                page = paginator.page(paginator.num_pages)
            else:
                page_num = 1
                page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        page_num = int(page_num)
        if page_num < 6:
            if paginator.num_pages <= 10:
                dis_range = range(1, paginator.num_pages + 1)
            else:
                dis_range = range(1, 11)
        elif page_num >= 6 and page_num <= paginator.num_pages - 5:
            dis_range = range(page_num - 5, page_num + 5)
        else:
            dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        context = {'page': page, 'dis_range': dis_range, 'article': article}
        # return render(request, '../templates/blog/district.html', context)
        return render(request, '../templates/blog/index.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('<h3>没有找到对应信息！</h3>')


def setCookie(request):
    response = HttpResponse('set cookie')
    response.set_cookie('a', 'abc')
    print(request.COOKIES.get('a', None))
    return response


def reqtest(request):
    # return HttpResponse(request.headers['User-Agent'])
    print(request.GET['name'])
    return HttpResponse(request.GET)


def upload(request):
    return render(request, '../templates/blog/upload.html')


def dealfile(request):
    myfile = request.FILES.get('pic')
    if not myfile:
        return HttpResponse(
            '''
            <h3>上传失败！即将返回...</h3>
            <script>
                setTimeout("parent.location.href='/'",2000);
            </script>
            '''
        )
    dirname = './media/images/' + \
        str(time.localtime().tm_year) + '/' + \
        str(time.localtime().tm_mon) + '/'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filename = dirname + str(time.time()) + '.' + myfile.name.split('.').pop()
    content = open(filename, 'wb+')
    for chunk in myfile.chunks():
        content.write(chunk)
    content.close()
    return HttpResponse(
        '''
        <h3>上传成功！即将返回...</h3>
        <script>
            setTimeout("parent.location.href='/'",2000);
        </script>
        '''
    )


def pageinfo(request):
    # 注：Django3.2的paginator类新增一种方法get_elided_page_range
    try:
        dlist = []
        paginator = Paginator(dlist, 6)
        page_num = request.GET.get('page', default='1')
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e:
            page_num = 1
            page = paginator.page(page_num)
        except EmptyPage as e:
            if int(page_num) > paginator.num_pages:
                page = paginator.page(paginator.num_pages)
            else:
                page_num = 1
                page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        page_num = int(page_num)
        if page_num < 6:
            if paginator.num_pages <= 10:
                dis_range = range(1, paginator.num_pages + 1)
            else:
                dis_range = range(1, 11)
        elif page_num >= 6 and page_num <= paginator.num_pages - 5:
            dis_range = range(page_num - 5, page_num + 5)
        else:
            dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        context = {'page': page, 'dis_range': dis_range}
        # return render(request, '../templates/blog/district.html', context)
        return render(request, '../templates/blog/index.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('<h3>没有找到对应信息！</h3>')


def detail(request, id):
    # article = get_object_or_404(Article, pnum=pnum)
    article = Article.objects.filter(id=id)
    return render(request, '../templates/blog/detail.html', context={'article': article})


def base(request):
    return render(request, '../templates/base.html')
