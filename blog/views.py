from django.db.models import base
from django.http import response
from django.http.response import Http404, HttpResponseServerError, JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import UserProfile
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.db.models import F  # 利用F来做自加1操作

import time
import os
import json
import hashlib
from urllib import parse
import base64

from blog.models import Article, SideBar, Tag, Category, ArticlePraise, ArticleStar

# Create your views here.


def reindex(request):
    return redirect(reverse('blog:index'))


def index(request):
    # 注：Django3.2的paginator类新增一种方法get_elided_page_range
    article = Article.objects.all().order_by('-created_time')
    paginator = Paginator(article, 5)
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
            response.set_cookie('uid', user.id)
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
    response.delete_cookie('uid')
    return response


def getUserInfo(request):
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
            'birthday': user.birthday,
            'gender': user.gender,
            'address': user.address,
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
    context = {
        'code': 1,
        'msg': 'success',
        'tab': tab,
        'spaceData': {}
    }

    if tab == 'home':
        return render(request, '../templates/blog/space/home.html', context)

    elif tab == 'post':
        return render(request, '../templates/blog/space/post.html', context)

    elif tab == 'star':
        star_articles = []
        stars = ArticleStar.objects.filter(user__id=request.user.id)
        for star in stars:
            star_articles.append(star)
        context['spaceData']['star_articles'] = star_articles
        return render(request, '../templates/blog/space/star.html', context)

    elif tab == 'follow':
        return render(request, '../templates/blog/space/follow.html', context)

    elif tab == 'fans':
        return render(request, '../templates/blog/space/fans.html', context)
