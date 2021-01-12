from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.test1,name='home'),
    path('',views.home_view,name='home'),
    path('index/',views.index,name = 'index'),
    path('chap/<int:id>',views.chaptest,name ='chap'),
    path('nd/<int:id>',views.ndchap,name = 'noidung'),
    path('dangky/',views.SignUp,name = 'dangky'),
    path('dangnhap/',auth_view.LoginView.as_view(template_name = 'DangNhap.html'),name='dangnhap'),
    path('dangxuat/',auth_view.LogoutView.as_view(next_page ='/'),name = 'dangxuat'),
    path('theloai/<name>',views.TheLoai,name='theloai'),
    path('tacgia/<name>',views.tacgia, name = 'tacgia'),
    path('search/',views.search, name = 'search'),

]