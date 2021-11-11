from django.http import response
from django.http.response import Http404
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from blog.models import Blog
import time
import os

# Create your views here.


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
    pass
