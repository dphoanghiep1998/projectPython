from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.test1,name='home'),
    path('index/',views.index,name = 'index'),
    path('chap/<int:id>',views.chaptest,name ='chap'),
    path('nd/<int:id>',views.ndchap,name = 'noidung'),
    path('dangky/',views.SignUp,name = 'dangky'),
    path('dangnhap/',auth_view.LoginView.as_view(template_name = 'pages/DangNhap.html'),name='dangnhap'),
    path('dangxuat/',auth_view.LogoutView.as_view(next_page ='/home'),name = 'dangxuat')
]