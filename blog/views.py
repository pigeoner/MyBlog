from django.db.models import base
from django.forms import fields
from django.forms import models
from django.http import response
from django.http.response import Http404, HttpResponseServerError, JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import UserProfile
from django.forms.models import model_to_dict
from django.forms import Form
from django.core.serializers import serialize
from django.db.models import F  # 利用F来做自加1操作

import time
import os
import json
import hashlib
from urllib import parse
import base64

from blog.models import Article, SideBar, Tag, Category, ArticlePraise, ArticleStar, Follow, Fans

# Create your views here.


def reindex(request):
    return redirect(reverse('blog:index'))


def get_paginator(item, page_num, one_page_num):
    paginator = Paginator(item, one_page_num)
    page_num = page_num
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
    return page, dis_range


def index(request):
    # 注：Django3.2的paginator类新增一种方法get_elided_page_range
    article = Article.objects.all().order_by('-created_time')
    page_num = request.GET.get('page', default='1')
    page, dis_range = get_paginator(article, page_num, 5)
    context = {'page': page, 'dis_range': dis_range}
    return render(request, '../templates/blog/index.html', context)


def about(request):
    with open('templates/blog/about.md', 'r') as ab:
        content = ab.read()
    context = {'content': content}
    return render(request, '../templates/blog/about.html', context)

def edit(request):
    from mdeditor.fields import MDTextFormField
    class MDEditorForm(Form):
        content = MDTextFormField(label='内容')
    context = {
        'form': MDEditorForm(),
        'tags': Tag.objects.all(),
        'category': Category.objects.all()
    }
    return render(request,'../templates/blog/edit.html', context)

def add(request):
    def user_directory_path(instance, filename):
        ext = filename.split('.').pop()
        filename = '{0}.{1}'.format(
            'cover/post_'+str(instance.user)+'_'+str(int(time.time())), ext)
        return filename
    user = UserProfile.objects.get(id=request.user.id)
    body = request.POST.get('body')
    category = request.POST.get('category')
    category = Category.objects.get(name=category)
    tags = request.POST.get('tags')
    tags = Tag.objects.filter(name=tags)
    cover = request.POST.get('cover')
    print(type(cover))
    # post = Article.objects.create(user=user, title='123', category=category, body=body, img='cover/Django.jpg')
    # post.tags.set(tags) # 设置多对多的tags
    return JsonResponse({'code': 1, 'msg': 'success'})


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
    userId = request.user.id
    isPraise = False
    isStar = False
    if userId:
        isUserPraise = ArticlePraise.objects.filter(article__id=post.id)
        isUserStar = ArticleStar.objects.filter(article__id=post.id)
        isPraise = True if isUserPraise else False
        isStar = True if isUserStar else False
    post.increase_views()
    return render(request, "../templates/blog/detail.html", {"post": post, "isPraise": isPraise, "isStar": isStar})


def archives(request, year, month):
    # 文章归档列表页
    post_list = Article.objects.filter(
        created_time__year=year, created_time__month=month)
    context = {'post_list': post_list, 'year': year, 'month': month}
    return render(request, '../templates/blog/archives_list.html', context)


def userLogin(request):
    if request.method == 'POST':   # 判断采用的是何种请求
        # request.POST[]或request.POST.get()获取数据
        username = request.POST['username']
        password = request.POST['password']
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(request, username=username, password=password)

        # userInfo = model_to_dict(UserProfile.objects.get(id=user.id))
        # userInfo['image'] = str(userInfo['image'])

        # 验证如果用户不为空
        if user is not None and user.is_active:
            # login方法登录
            login(request, user)
            # 返回登录成功信息
            response = HttpResponse(json.dumps({
                "code": "1",
                "msg": "success",
            }))
            userDetail = UserProfile.objects.get(id=user.id)
            articleCount = len(Article.objects.filter(user__id=user.id))
            followCount = len(Follow.objects.filter(user__id=user.id))
            fansCount = len(Fans.objects.filter(user__id=user.id))
            userInfo = {
                "nickname": base64.b64encode(userDetail.nick_name.encode('utf8')).decode('utf8'),
                "avatar": str(userDetail.image),
                "articleCount": articleCount,
                "followCount": followCount,
                "fansCount": fansCount
            }
            response.set_cookie('USER_INFO', userInfo,
                                max_age=14*24*60*60)
            return response
        else:
            # 返回登录失败信息
            return HttpResponse(json.dumps({
                "code": "0",
                "msg": "error"
            }))


def userLogout(request):
    logout(request)
    response = JsonResponse({
        'code': '1',
        'msg': 'success'
    })
    response.delete_cookie('USER_INFO')
    return response


def toolbarUserInfo(request):
    user = UserProfile.objects.get(id=request.user.id)

    followCount = 0
    fansCount = 0

    praiseCount = 0
    commentsCount = 0
    starCount = 0

    for post in Article.objects.filter(user=user):
        praiseCount += post.thumbs_up
        commentsCount += post.comments
        starCount += post.star

    # def bigNumDeal(count):
    #     num = count
    #     if num > int(1e4):
    #         if num < int(1e8):
    #             num = str(int(num / 1e4)) + '.' + \
    #                 str(int((num % 1e4) / 1000)) + '万'
    #         else:
    #             num = str(int(num / 1e8)) + '.' + \
    #                 str(int((num % 1e8) / 1e7)) + '亿'
    #     return num

    response = JsonResponse({
        'code': '1',
        'msg': 'success',
        'data': {
            'uid': user.id,
            'nickname': user.nick_name,
            'image': str(user.image),
            'sign': user.sign,
            'followCount': followCount,
            'fansCount': fansCount,
            'praiseCount': praiseCount,
            'commentsCount': commentsCount,
            'starCount': starCount,
        }
    })

    return response


def praise(request):
    articleId = request.POST.get('articleId')
    # 点赞人即当前登陆人
    user = UserProfile.objects.get(id=request.user.id)
    print(user)
    article = Article.objects.get(id=articleId)

    # 过滤已经点赞或者踩了的
    obj = ArticlePraise.objects.filter(
        user__id=request.user.id, article__id=articleId).first()
    # 返回json
    response = {'code': 1, 'msg': '点赞成功', 'isPraise': True}

    if not obj:
        ArticlePraise.objects.create(user=user, article=article)
        # 生成了赞记录， 然后再来更新页面
        Article.objects.filter(id=articleId).update(thumbs_up=F('thumbs_up')+1)
    else:
        ArticlePraise.objects.filter(
            user__id=request.user.id, article__id=articleId).delete()
        Article.objects.filter(id=articleId).update(thumbs_up=F('thumbs_up')-1)
        response = {'code': 0, 'msg': '撤销点赞', 'isPraise': False}

    return JsonResponse(response)  # 必须用json返回


def star(request):
    articleId = request.POST.get('articleId')
    # 点赞人即当前登陆人
    user = UserProfile.objects.get(id=request.user.id)
    article = Article.objects.get(id=articleId)

    # 过滤已经点赞或者踩了的
    obj = ArticleStar.objects.filter(
        user__id=request.user.id, article__id=articleId).first()
    # 返回json
    response = {'code': 1, 'msg': '收藏成功', 'isStar': True}

    if not obj:
        ArticleStar.objects.create(user=user, article=article)
        # 生成了赞记录， 然后再来更新页面
        Article.objects.filter(id=articleId).update(star=F('star')+1)
    else:
        ArticleStar.objects.filter(
            user__id=request.user.id, article__id=articleId).delete()
        # 生成了赞记录， 然后再来更新页面
        Article.objects.filter(id=articleId).update(star=F('star')-1)
        response = {'code': 0, 'msg': '撤销收藏', 'isStar': False}

    return JsonResponse(response)  # 必须用json返回


def space(request):
    tab = request.GET.get('tab', default='home')
    user = UserProfile.objects.get(id=request.user.id)

    followCount = 0
    fansCount = 0

    praiseCount = 0
    commentsCount = 0
    starCount = 0

    for post in Article.objects.filter(user=user):
        praiseCount += post.thumbs_up
        commentsCount += post.comments
        starCount += post.star

    context = {
        'tab': tab,
        'userInfo': {
            'uid': user.id,
            'nickname': user.nick_name,
            'birthday': user.birthday,
            'gender': user.gender,
            'address': user.address,
            'sign': user.sign,
            'followCount': followCount,
            'fansCount': fansCount,
            'praiseCount': praiseCount,
            'commentsCount': commentsCount,
            'starCount': starCount,
        }
    }

    if tab == 'home':
        return render(request, '../templates/blog/space/home.html', context)

    elif tab == 'post':
        posts = Article.objects.filter(
            user__id=request.user.id).order_by('-created_time')
        page_num = request.GET.get('page', default='1')
        page, dis_range = get_paginator(posts, page_num, 5)
        context['page'] = page
        context['dis_range'] = dis_range
        return render(request, '../templates/blog/space/post.html', context)

    elif tab == 'star':
        stars = ArticleStar.objects.filter(
            user__id=request.user.id).order_by('-starTime')
        page_num = request.GET.get('page', default='1')
        page, dis_range = get_paginator(stars, page_num, 5)
        context['page'] = page
        context['dis_range'] = dis_range
        return render(request, '../templates/blog/space/star.html', context)

    elif tab == 'follow':
        follows = Follow.objects.filter(
            user__id=request.user.id).order_by('-followTime')
        page_num = request.GET.get('page', default='1')
        page, dis_range = get_paginator(follows, page_num, 10)
        context['page'] = page
        context['dis_range'] = dis_range
        return render(request, '../templates/blog/space/follow.html', context)

    elif tab == 'fans':
        fans = Fans.objects.filter(
            user__id=request.user.id).order_by('-fansTime')
        page_num = request.GET.get('page', default='1')
        page, dis_range = get_paginator(fans, page_num, 10)
        context['page'] = page
        context['dis_range'] = dis_range
        return render(request, '../templates/blog/space/fans.html', context)
