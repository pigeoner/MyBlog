from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
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
