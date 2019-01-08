
from django.contrib import admin
from django.urls import path

from unid import views
from .views import *





urlpatterns = [
    path('mywallet/', mywallet,),
    path('', main, name='main'),
    path('main_upload', main_upload, name='main_upload'),
    path('contentsdetail/<int:id>', contentsdetail, name='contentsdetail'),
    path('contentstran/', contentstran, name='contentstran'),
    path('oauth', views.oauth, name='oauth'),
    path('login/', views.login, name='login'),
    path('transaction/', transaction),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('contentsupload/', views.contentsupload, name='contentsupload'),
    path('mypage/', views.mypage, name='mypage'),
    path('contentsboard/', contentsboard,   name='contentsboard'),
    path('searchcontents/<str:category>', views.searchcontents, name='searchcontents'),
    path('moneytrade/', views.moneytrade, name='moneytrade'),
    path('download/', views.download, name='download'),
    path('writereply/', views.writereply, name='writereply'),
]
