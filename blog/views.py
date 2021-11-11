from django.http import response
from django.http.response import Http404
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.models import Blog, District
import time
import os

# Create your views here.


def reindex(request):
    return redirect(reverse('blog:index'))


def index(request):
    # return redirect(reverse('blog:test', args=['chouba']))
    return render(request, '../templates/index.html')


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


def printStr(request, id):
    blog = Blog.objects.get(id=id)
    return HttpResponse(
        '''
        <html>
            <head>
                <title>print</title>
            </head>
            <body>
                <pre>{}</pre>
            </body>
        </html>
        '''.format(blog)
    )


def test404(request):
    raise Http404('404')


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
        dlist = District.objects.filter()
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
        return render(request, '../templates/blog/district.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('<h3>没有找到对应信息！</h3>')
