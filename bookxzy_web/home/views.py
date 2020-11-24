from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book,Chapter
from .form import Dangky
import os
# Create your views here.
def home_view(request):
    return render(request,'pages/home.html')
def index(request):
    return render(request,'pages/index.html')
def test1(request):
    book = Book.objects.all()
    context = {'book':book}
    return render(request,'pages/home.html',context)
def chaptest(request,id):
    book = Book.objects.get(pk=id)
    context = {'book':book}
    return render(request,'pages/chaptest.html',context)
def ndchap(request, id):
    chapper = Chapter.objects.get(pk=id)
    noidung = chapper.content.read().decode('utf-8')
    context = {'noidung':noidung,'title':chapper.title}
    return render(request,'pages/noidung.html',context)
def SignUp(request):
    form = Dangky()
    if request.method == 'POST':
        form = Dangky(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/dangnhap')
    context = {'form':form}
    return render(request,'pages/Dangky.html',context)