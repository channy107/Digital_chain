
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from unid import views
from .views import *
from haystack.views import SearchView




urlpatterns = [
    path('mywallet/', views.mywallet, name='mywallet'),
    path('', main, name='main'),
    path('main_upload', main_upload, name='main_upload'),
    path('main_detail/<int:id>', main_detail, name='main_detail'),
    path('mainreply/', mainreply, name='maineply'),
    path('voting/', voting, name='voting'),
    path('contentsdetail/<int:id>', contentsdetail, name='contentsdetail'),
    path('contentstran/', contentstran, name='contentstran'),
    path('login/', views.login, name='login'),
    path('transaction/', views.transaction, name='transaction'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('contentsupload/', views.contentsupload, name='contentsupload'),
    path('postmodify/<int:id>', views.postmodify, name='postmodify'),
    path('postdelete/', views.postdelete, name='postdelete'),
    path('mypage/', views.mypage, name='mypage'),
    path('contentsboard/', contentsboard,   name='contentsboard'),
    path('searchcontents/<str:category>', views.searchcontents, name='searchcontents'),
    path('moneytrade/', views.moneytrade, name='moneytrade'),
    path('download/', views.download, name='download'),
    path('writereply/', views.writereply, name='writereply'),
    path('exchange/', views.exchange, name='exchange'),
    path('purchase/', views.purchase, name='purchase'),
    path('download/', views.download, name='download'),
    path('my_cron_job/', my_cron_job, name='my_cron_job'),
]
