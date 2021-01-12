from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book,Chapter,Category
from .form import Dangky
import os
# Create your views here.
def home_view(request):
    return render(request,'home.html')
def test1(request):
    book = Book.objects.all()
    category = Category.objects.all()
    context = {'book':book,'cate':category}
    return render(request,'home.html',context)
def chaptest(request,id):
    book = Book.objects.get(pk=id)
    context = {'book':book}
    return render(request,'chaptest.html',context)
def ndchap(request, id):
    chapper = Chapter.objects.get(pk=id)
    noidung = chapper.content.read().decode('utf-8')
    context = {'noidung':noidung,'title':chapper.title}
    return render(request,'noidung.html',context)
def SignUp(request):
    form = Dangky()
    if request.method == 'POST':
        form = Dangky(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/dangnhap')
    context = {'form':form}
    return render(request,'Dangky.html',context)

def TheLoai(request,name): #Lọc theo thể loại
    category = Category.objects.get(name=name)
    Bookcate = category.book_set.all()
    cate = Category.objects.all()
    cateall = Category.objects.all()
    contex = {'bookcate':Bookcate,'cate':cate,'cateall':cateall}
    return render(request,'theloai.html',contex)


