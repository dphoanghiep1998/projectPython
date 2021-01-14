from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book,Chapter,Category,Author
from .form import Dangky,CommentForm,uploadbook
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import inlineformset_factory
import os
from django.contrib.auth.models import User
# Create your views here.
def home_view(request):
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

def test1(request): #Hiển thị sách
    booklist = Book.objects.all().order_by('-createDate')
    bookhot = Book.objects.all().order_by('-click')
    if len(bookhot) >=6:
        booknew = bookhot[0:5]
    else:
        booknew = bookhot[0:len(bookhot)]
    category = Category.objects.all()
    author = Author.objects.all()
    paginator = Paginator(booklist, 12)
    pageNumber = request.GET.get('page')
    try:
        book = paginator.page(pageNumber)
    except PageNotAnInteger:
        book = paginator.page(1)
    except EmptyPage:
        book = paginator.page(paginator.num_pages)

    context = {'book':book,'cate': category,'author':author,"booknew":booknew}
    return render(request,'home.html',context)

def hot(request): #Hiển thị sách
    booklist = Book.objects.all().order_by('-click')
    bookhot = Book.objects.all().order_by('-createDate')
    if len(bookhot) >=6:
        booknew = bookhot[0:5]
    else:
        booknew = bookhot[0:len(bookhot)]
    category = Category.objects.all()
    author = Author.objects.all()
    paginator = Paginator(booklist, 12)
    pageNumber = request.GET.get('page')
    try:
        book = paginator.page(pageNumber)
    except PageNotAnInteger:
        book = paginator.page(1)
    except EmptyPage:
        book = paginator.page(paginator.num_pages)
        
    context = {'book':book,'cate': category,'author':author,"booknew":booknew}
    return render(request,'truyenhot.html',context)


def chaptest(request,id): #Hiển thị danh sách chương
    book = Book.objects.get(pk=id)
    book.click +=1
    book.save()
    cate = Category.objects.all()
    catesame = book.category.all()[0]
    booksame = catesame.book_set.all().exclude(pk = book.id).order_by('-createDate')
    if len(booksame) >=4:
        bsame = booksame[0:3]
    elif len(booksame) < 4 and len(booksame)>0:
        bsame = booksame[0:len(booksame)]
    else:
        bsame = None
    chap = book.chapter_set.all().order_by('-order')
    first = chap[len(chap)-1]
    form = CommentForm()
    comment = book.comment.all().order_by('-time_pub')
    if request.method == "POST":
        form = CommentForm(request.POST,author=request.user,book = book) # author=request.user,book = book  viết như vậy dữ liệu sẽ đc lưu trong **kwargs
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    context = {'book': book, 'chap': chap,'form':form,'comment':comment,'cate':cate,'first':first,'booksame':bsame}
    return render(request,'chaptest.html',context)

def ndchap(request, id): # Hiển thị nội dung chương
    chapper = Chapter.objects.get(pk=id)
    book = Book.objects.filter(chapter = chapper)
    cate = Category.objects.all()
    book = book[0]
    chap = book.chapter_set.all()
    for i in range(len(chap)-1): # taọ nút next và pre
        if chap[i] == chapper and i != 0:
            next = chap[i+1].id
            pre = chap[i-1].id
            break
        if chap[i] == chapper and i == 0:
            next =  chap[i+1].id
            pre =  None
            break
        else:
            next = None
            pre = chap[len(chap)-2].id

    noidung = chapper.content.read().decode('utf-8')
    line = chapper.title
    context = {'noidung': noidung, 'title': chapper.title, 'book': book,'chap':chapper,'next':next,'pre':pre,
               'line':line,'cate':cate}

    return render(request,'noidung.html',context)

def SignUp(request): # Đăng ký tài khoản
    form = Dangky()
    if request.method == 'POST':
        form = Dangky(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dangnhap')
    context = {'form':form}
    return render(request,'Dangky.html',context)

def TheLoai(request,name): #Lọc theo thể loại
    category = Category.objects.get(name=name)
    Bookcate = category.book_set.all()
    cate = Category.objects.all()
    paginator = Paginator(Bookcate, 8)
    pageNumber = request.GET.get('page')
    try:
        book = paginator.page(pageNumber)
    except PageNotAnInteger:
        book = paginator.page(1)
    except EmptyPage:
        book = paginator.page(paginator.num_pages)


    contex = {'bookcate':book,'cate':cate,'category':category}
    return render(request,'theloai.html',contex)


def tacgia(request,name): #Lọc theo tác giả
     author = Author.objects.get(Name = name)
     book = author.book_set.all()
     cate = Category.objects.all()
     contex = {'book':book,'author':author,'cate':cate}
     return render(request,'tacgia.html',contex)

def search(request):
    cate = Category.objects.all()
    if request.method == 'GET':
        searchtext = request.GET.get('search', None)
        if searchtext:
            book = Book.objects.filter(BookName__icontains = searchtext)
        else:
            book = None
        context = {'book': book,'searchtext':searchtext,'cate':cate}
        return render(request, 'search.html', context)

def up_books(request):
    book = Book()
    book_form = uploadbook(instance=book) # setup a form for the parent
    ChapterInlineFormSet = inlineformset_factory(Book, Chapter, fields=('title','content','order','time_pub'), extra=1)
    formset = ChapterInlineFormSet(instance=book)
    if request.method == "POST":
        book_form = uploadbook(request.POST,request.FILES)
        formset = ChapterInlineFormSet(request.POST, request.FILES)
        if book_form.is_valid():
            created_book = book_form.save(commit=True)
            formset = ChapterInlineFormSet(request.POST, request.FILES, instance=created_book )
            if formset.is_valid():
                created_book.userid = request.user.id
                created_book.save()
                formset.save()
                so = 0
                chap = created_book.chapter_set.all()
                if len(chap) != 0:
                    so = chap[len(chap) - 1].order
                for afile in request.FILES.getlist('multiple'):
                    so += 1
                    line = "Chương " + str(so)
                    instance = Chapter(title=line, book=created_book, content=afile, order=so)
                    instance.save()
                return HttpResponse("upload thanh cong")

    return render(request,"upload.html", {
        "book_form": book_form,
        "form": formset,
    })


def goiUser(request,id):

    return render(request,"profile.html")

def edit_book(request,id):
    book = Book.objects.get(pk = id)
    book_form = uploadbook(instance=book) # setup a form for the parent
    ChapterInlineFormSet = inlineformset_factory(Book, Chapter, fields=('title','content','order','time_pub'), extra=1)
    formset = ChapterInlineFormSet(instance=book)
    if request.method == "POST":
        book_form = uploadbook(request.POST,request.FILES,instance=book)
        formset = ChapterInlineFormSet(request.POST, request.FILES)
        if book_form.is_valid():
            created_book = book_form.save(commit=False)
            formset = ChapterInlineFormSet(request.POST, request.FILES, instance=created_book )
            if formset.is_valid():
                created_book.userid = request.user.id
                created_book.save()
                formset.save()
                so = 0
                chap = created_book.chapter_set.all()
                if len(chap) != 0:
                    so = chap[len(chap) - 1].order
                for afile in request.FILES.getlist('multiple'):
                    so += 1
                    line = "Chương " + str(so)
                    instance = Chapter(title=line, book=created_book, content=afile, order=so)
                    instance.save()
                return HttpResponse("upload thanh cong")

    return render(request,"edit.html", {
        "book_form": book_form,
        "form": formset,
    })
def infoUser(request,use):
    book =  Book.objects.filter(userid = use)
    book2 = Book.objects.all()
    context = {"book":book,"book2":book2}
    return render(request,"infor.html",context)