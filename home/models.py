from django.core.exceptions import ValidationError
from django.db import models
from .validators import validate_ContentChapter
import datetime
from os.path import join as osjoin
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect

class Author(models.Model):
    Name = models.CharField(max_length=100)
    birth = models.DateField(default=None,null=True,blank=True)
    def __str__(self):
        return self.Name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.name





class Book(models.Model):
    status_choice = ((0,"Đang ra"),(1,"Đã hoàn thành"),(2,"Tạm ngưng"))
    BookName = models.CharField(max_length=100)
    createDate = models.DateTimeField(default=datetime.datetime.now())
    imageBook = models.ImageField(upload_to='image/%Y/%m/%d/',blank=True,null=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,default= None,blank=True,null=True)
    category = models.ManyToManyField(Category)
    status = models.IntegerField(choices=status_choice,default=0)
    def __str__(self):
        return self.BookName

class Chapter(models.Model):
    def book_upload(self, filename):# Tạo vị trí lưu của chapter ứng với truyện
        return osjoin(str(self.book.BookName),filename)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.FileField(upload_to=book_upload,validators=[validate_ContentChapter]) #documents/%Y/%m/%d/:Chỉ định nơi lưu file , tệp documents sẽ dc tạo tự động trong media
    order = models.IntegerField(default=0)
    time_pub = models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        ordering = ["order"]
    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="comment",default=None)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE,default=None)
    content = models.TextField(max_length=1000)
    time_pub = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Bạn không thể thay đổi trường này" )
        super(Comment, self).save(*args, **kwargs)


