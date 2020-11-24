from django.contrib import admin
from .models import Book,Author,Category,Chapter,Comment
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['Name','birth']
    search_fields = ['Name']



class ChapterInlines(admin.TabularInline):
    model = Chapter
    classes = ['collapse']
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ['BookName' ,'createDate'] # Hiển thị của book trên trang admin
    list_filter = ['createDate']  #Thanh bar dọc tìm kiếm theo ngày
    search_fields = ['BookName'] # thanh search bar tìm kiếm theo tên sách
    fieldsets = [
        ('Tên Sách',{'fields':['BookName']}),('Ngày tạo',{'fields':['createDate']}),
        ('Bìa sách',{'fields':['imageBook']}),('Tác giả',{'fields':['author']}),
        ('Thể loại',{'fields':['category'],'classes': ['collapse']})  # Phân chia các trường trên trang admin
    ]
    inlines = [ChapterInlines] # Đưa chapter vào Book trên trang admin



admin.site.register(Book,BookAdmin) #Tích hợp BookAdmin đã tạo ở trên
admin.site.register(Author,AuthorAdmin)
admin.site.register(Category)
admin.site.register(Comment)

