import re
import datetime
from django.contrib import admin
from .models import Book,Author,Category,Chapter,Comment
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['Name','birth']
    search_fields = ['Name']



class ChapterInlines(admin.TabularInline):
    model = Chapter
    classes = ['collapse'] #collapse : Cuộn nội dung này
    extra = 0
class CommentInline(admin.TabularInline):
    model = Comment
    classes = ['collapse'] #collapse : Cuộn nội dung này
    extra = 0



class BookAdmin(admin.ModelAdmin):
    list_display = ['BookName' ,'createDate'] # Hiển thị của book trên trang admin
    list_filter = ['createDate']  #Thanh bar dọc tìm kiếm theo ngày
    search_fields = ['BookName'] # thanh search bar tìm kiếm theo tên sách
    fieldsets = [
        ('Tên Sách',{'fields':['BookName']}),('Ngày tạo',{'fields':['createDate']}),
        ('Mô tả', {'fields': ['description']}),
        ('Trạng thái',{'fields': ['status']}),
        ('Bìa sách',{'fields':['imageBook']}),('Tác giả',{'fields':['author']}),
        ('Thể loại',{'fields':['category'],'classes': ['collapse']}),  # Phân chia các trường trên trang admin
        ('Lượt xem', {'fields': ['click']})
    ]
    inlines = [ChapterInlines,CommentInline,] # Đưa chapter vào Book trên trang admin

    def save_model(self, request, obj, form, change):
        obj.save()
        so = 0
        chap = obj.chapter_set.all()
        if len(chap) != 0:
            so = chap[len(chap)-1].order

        for afile in request.FILES.getlist('multiple'):
            # name = afile.name.split("/")
            # name = name[-1].split(".")
            # # name = name[0]
            # line = afile.readline().decode('utf-8').rstrip()
            # while not line:
            #     line = afile.readline().rstrip().decode('utf-8').rstrip().strip()

            # line = line.replace(":", " ")
            so +=1
            line = "Chương " + str(so)

            instance = Chapter(title = line ,book = obj , content = afile,order = so)
            instance.save()


admin.site.register(Book,BookAdmin) #Tích hợp BookAdmin đã tạo ở trên
admin.site.register(Author,AuthorAdmin)
admin.site.register(Category)
admin.site.register(Comment)