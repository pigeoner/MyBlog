from django.http import response
from django.http.response import Http404, HttpResponseServerError
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import UserProfile
from django.forms.models import model_to_dict
from django.core.serializers import serialize

import time
import os
import json
import hashlib

from blog.models import Article, SideBar, Tag, Category

# Create your views here.


def reindex(request):
    return redirect(reverse('blog:index'))
    # return redirect(reverse('blog:base'))


def index(request):
    # 注：Django3.2的paginator类新增一种方法get_elided_page_range
    article = Article.objects.all().order_by('-created_time')
    paginator = Paginator(article, 10)
    page_num = request.GET.get('page', default='1')
    try:
        page = paginator.get_page(page_num)
    except PageNotAnInteger as e:
        page_num = 1
        page = paginator.get_page(page_num)
    except EmptyPage as e:
        if int(page_num) > paginator.num_pages:
            page = paginator.get_page(paginator.num_pages)
        else:
            page_num = 1
            page = paginator.get_page(page_num)
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
    return render(request, '../templates/blog/index.html', context)


def setCookie(request):
    response = HttpResponse('set cookie')
    response.set_cookie('a', 'abc')
    print(request.COOKIES.get('a', None))
    return response


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


def detail(request, id):
    post = Article.objects.get(id=id)
    post.increase_views()
    print('----------------increase------------------')
    return render(request, "../templates/blog/detail.html", {"post": post, "increase_thumbs_up": post.increase_thumbs_up})


def archives(request, year, month):
    # 文章归档列表页
    post_list = Article.objects.filter(
        created_time__year=year, created_time__month=month)
    context = {'post_list': post_list, 'year': year, 'month': month}
    return render(request, '../templates/blog/archives_list.html', context)


def userlogin(request):
    if request.method == 'POST':   # 判断采用的是何种请求
        # request.POST[]或request.POST.get()获取数据
        username = request.POST['username']
        password = request.POST['password']
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(request, username=username, password=password)

        userInfo = model_to_dict(UserProfile.objects.get(id=user.id))
        userInfo['image'] = str(userInfo['image'])

        # 验证如果用户不为空
        if user is not None and user.is_active:
            # login方法登录
            login(request, user)
            # 返回登录成功信息
            response = HttpResponse(json.dumps({
                "code": "1",
                "msg": "success",
                # "userInfo": userInfo,
            }))
            response.set_cookie('avatar', userInfo['image'], max_age=7*24*3600)
            response.set_cookie(
                'username', userInfo['nick_name'], max_age=7*24*3600)
            return response
            return
        else:
            # 返回登录失败信息
            return HttpResponse(json.dumps({
                "code": "0",
                "msg": "error"
            }))
