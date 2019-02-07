
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from unid import views
from .views import *
# from haystack.views import SearchView




urlpatterns = [
    path('mywallet/', views.mywallet, name='mywallet'),
    path('', main, name='main'),
    path('main_upload/', main_upload, name='main_upload'),
    path('info_popular/', info_popular, name='info_popular'),
    path('information/', information, name='information'),
    path('infotag/<str:category>', infotag, name='infotag'),
    path('main_upload', main_upload, name='main_upload'),
    path('main_detail/<int:id>', main_detail, name='main_detail'),
    path('mainreply/', mainreply, name='maineply'),
    path('voting/', voting, name='voting'),
    path('vote/', vote, name='vote'),
    path('contentsdetail/<int:id>', contentsdetail, name='contentsdetail'),
    path('transaction/', views.transaction, name='transaction'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('contentsupload/', views.contentsupload, name='contentsupload'),
    path('postmodify/<int:id>', views.postmodify, name='postmodify'),
    path('postdelete/', views.postdelete, name='postdelete'),
    path('mypage/', views.mypage, name='mypage'),
    path('user_detail/<int:id>', views.user_detail, name='user_detail'),
    path('contentsboard/', contentsboard,   name='contentsboard'),
    path('searchcontents/<str:category>', views.searchcontents, name='searchcontents'),
    path('moneytrade/', views.moneytrade, name='moneytrade'),
    path('download/', views.download, name='download'),
    path('writereply/', views.writereply, name='writereply'),
    path('exchange/', views.exchange, name='exchange'),
    path('purchase/', views.purchase, name='purchase'),
    path('download/', views.download, name='download'),
    path('my_cron_job/', my_cron_job, name='my_cron_job'),
    path('test_validfile/', views.test_validfile, name='test_validfile'),
    path('termsofuse/', views.termsofuse, name='termsofuse'),
    path('privacy/', views.privacy, name='privacy'),
    path('unidadmin/', views.unidAdmin, name='unidAdmin'),
    path('opinion/', views.opinion, name='opinion'),
    path('warninguser/', views.warninguser, name='warninguser'),
    path('noProblem/', views.noProblem, name='noProblem'),
    path('testpage/', views.testpage, name='testpage'),
    path('contentsBlockTest/', views.contentsBlockTest, name='contentsBlockTest'),
    path('user_name_verification/', views.user_name_verification, name='user_name_verification'),
    path('loginAdmin/', views.loginAdmin, name='loginAdmin'),
    path('commandMysql/', views.commandMysql, name='commandMysql'),
    path('funding/', views.funding, name='funding'),
    # path('friendsearch', views.FriendSearch, name='friendsearch')
    # path('seach/autocomplete', views.autocomplete, name='autocomplete')

]
