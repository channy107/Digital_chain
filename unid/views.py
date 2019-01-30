import os
from _sha256 import sha256
from datetime import datetime, time
from ftplib import FTP
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
import time
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from web3 import Web3, HTTPProvider
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
import zipfile
from unidweb import settings
from .models import *
import random
from django.shortcuts import render
import hashlib
from allauth.account.signals import user_logged_in, user_logged_out
import pyminizip
import shutil

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured

from .mixins import ActiveOnlyMixin

class MyView(ActiveOnlyMixin, View):
    permission_denied_message = 'You must be logged in to view this page'
    not_activated_message = 'You haven\'t activated your account yet'

    not_activated_redirect = 'accounts:inactive_registration'





def logged_in(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']
    member = myPageInfomation.objects.get(user=user)
    request.session['user_email'] = member.email
    request.session['user_name'] = member.name
user_logged_in.connect(logged_in, sender=User)


# def logged_out(sender, **kwargs):
#     request.session['user_email'] = {}
#     request.session.modified = True
# user_logged_out.connect(logged_out, sender=User)



@login_required
def mypage(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        contentsboard = uploadContents.objects.filter(writeremail_id=request.session['user_email'])[:3]
        articles = Post.objects.order_by('-posts_id').filter(user_id=request.session['user_email'])[:3]
        numbersOfArticles = len(Post.objects.filter(user_id=request.session['user_email']))
        myreward = walletInFormation.objects.filter(type='reward', toAccount=mypage.account)
        contents_transfer = walletInFormation.objects.filter(type='contentsTransaction')
        replies = replyForPosts.objects.order_by('-IDX').filter(user_id=request.session['user_email'])
        downloads = downloadContents.objects.order_by('-IDX').filter(downloader_email_id=request.session['user_email'])[:3]
        context = {'articles':articles,
                   'myreward':myreward,
                   'mypage':mypage,
                   'numbersOfArticles':numbersOfArticles,
                   'contentsboard':contentsboard,
                   'downloads':downloads,
                   'replies':replies,
                   'contents_transfer':contents_transfer
                   }
        return render(request, 'unid/mypage.html', context)

    else:


        if request.FILES.get('user_image_upload'):

            userimage = request.FILES.get('user_image_upload')
            with open("media/imagesForUserProfile" + "/" + userimage.name, 'wb') as file:
                for chunk in userimage.chunks():
                    file.write(chunk)

            user_email = myPageInfomation.objects.filter(email=request.session['user_email'])
            update = user_email.update(
            userimage = "media/imagesForUserProfile" + "/" + userimage.name)

        if request.FILES.get('background'):
            background = request.FILES.get('background')
            with open("media/imagesForUserProfile" + "/" + background.name, 'wb') as file2:
                for chunk in background.chunks():
                    file2.write(chunk)

            myPageInfomation.objects.filter(email=request.session['user_email']).update(
            aaa = "media/imagesForUserProfile" + "/" + background.name)


        # user_profiles = myPageInfomation.objects.values('name')
        # # if user_profiles:
        # #     return HttpResponse(user_profiles)
        # user_name = request.POST['name']
        # user_profile = request.POST['profile'],
        # for nameaa in user_profiles:
        #     if user_name == nameaa:
        #         return HttpResponse('중복된 이름입니다.')
        #     else:
        #         myPageInfomation.objects.filter(email=request.session['user_email']).update(
        #             name=request.POST['name'],
        #             profile=request.POST['profile'],
        #             last_modified=timezone.now()
        #         )

        myPageInfomation.objects.filter(email=request.session['user_email']).update(
            name = request.POST['name'],
            profile = request.POST['profile'],
            last_modified = timezone.now()
        )


        url = '/unid/mypage'
        return HttpResponseRedirect(url)



def termsofuse(request):
    return render(request, 'unid/termsofuse.html')

def privacy(request):
    return render(request, 'unid/privacy.html')



def contentsboard(request):
    contentsboard = uploadContents.objects.all()
    mypage = myPageInfomation.objects.get(email=request.session['user_email'])
    context = {'contentsboard': contentsboard, 'mypage':mypage}
    return render(request, 'unid/contentsboard.html', context)

@login_required
def mywallet(request):
    walletInfo = walletInFormation.objects.all()
    walletcount = walletInFormation.objects.count()
    mypage = myPageInfomation.objects.get(email=request.session['user_email'])

    # html = ''
    # for info in walletInfo:
    #     info.transactiondate = timezone.now()
    #     html += str(info.transactiondate) + '<br>' + info.fromAccount + '<br>' +info.toAccount + '<br>'+ str(info.balance) + '<br>'+ info.txid
    return render(request,'unid/mywallet.html', {'list':walletInfo, 'count':walletcount, 'mypage':mypage})

@login_required
def transaction(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(request, 'unid/transaction.html', {'mypage':mypage})
    else:
        from_account = request.POST['from_account']
        to_account = request.POST['to_account']
        account_bal = request.POST['account_bal']
        tran_id = request.POST['tran_id']

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)

        transactionData = walletInFormation(fromAccount=from_info.email, toAccount=to_info.email, balance=account_bal,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("coinTransaction")
        transactionData.save()

    return render(request, 'unid/transaction.html', {})

@login_required
def exchange(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(request, 'unid/exchange.html', {'mypage':mypage})
    else:
        from_account = request.POST['e_from_account']
        to_account = request.POST['e_to_account']
        account_bal = request.POST['e_account_bal']
        tran_id = request.POST['e_tran_id']

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)

        transactionData = walletInFormation(fromAccount=from_info.email, toAccount=to_info.email, balance=account_bal,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("exchange")
        transactionData.save()

    return render(request, 'unid/exchange.html', {})

@login_required
def purchase(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(request, 'unid/purchase.html', {'mypage':mypage})
    else:
        from_account = request.POST['p_from_account']
        to_account = request.POST['p_to_account']
        account_bal = request.POST['p_account_bal']
        tran_id = request.POST['p_tran_id']

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)

        transactionData = walletInFormation(fromAccount=from_info.email, toAccount=to_info.email, balance=account_bal,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("purchase")
        transactionData.save()
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])


    return render(request, 'unid/purchase.html', {'mypage':mypage})

def contentsdetail(request, id):
    contents = uploadContents.objects.get(contents_id=id)
    replys = replysForContents.objects.filter(contents_id=id).values()
    contents.hits = contents.hits + 1  # 조회수 증가
    contents.save()

    previewlist = []
    if previewInfo.objects.filter(contents_id=id).values():
        for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
            previewimage = previewInfo.objects.filter(contents_id=id).values()[i]['imagepath']
            previewlist.append(previewimage)
        first_preview = previewlist[0]
        try:
            second_preview = previewlist[1]
        except IndexError as e:
            second_preview = ""
        try:
            third_preview = previewlist[2]
        except IndexError as e:
            third_preview = ""
    else:
        first_preview = 'media/default.png'
        second_preview = 'media/default.png'
        third_preview = 'media/default.png'
    files_infos = contentsInfo.objects.filter(contents_id=id).values()

    rpc_url = "http://222.239.231.252:9545"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x5bf8997775c7dcb7a39e68fc5c43479ceb45eed1")
    ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}]
)

    try:
        account = Web3.toChecksumAddress(myPageInfomation.objects.get(email=request.session['user_email']).account)
    except KeyError as e:
        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'files_infos': files_infos, 'nid_balance': "로그인이 필요합니다"
             }
        )

    nid_balance = ncc.functions.balanceOf(account).call()     # contentsdetail.html 의 javascript 도 수정 (533)

    if downloadContents.objects.filter( Q(contents_id=id) & Q(downloader_email=request.session['user_email']) ):
        # contents_id = uploadContents.objects.get(contents_id=id).contents_id
        # title = uploadContents.objects.get(contents_id=id).title + ".zip"
        downloadid = str(random.random())
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'nid_balance': nid_balance,
             "downloadid": downloadid, 'files_infos': files_infos, 'mypage':mypage
             }
        )

               # contentsdetail.html 403 번 줄 부터 확인 필요
    else:
        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'files_infos': files_infos,
             'nid_balance': nid_balance
             }
        )

@require_POST
def moneytrade(request):
    rpc_url = "http://222.239.231.252:9545"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x5bf8997775c7dcb7a39e68fc5c43479ceb45eed1")
    ncc = w3.eth.contract(address = nidCoinContract_address, abi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}]
)

    writeremail = request.POST['writeremail']
    sellerinfo = myPageInfomation.objects.get(email=writeremail)
    price = uploadContents.objects.get(contents_id=request.POST['id']).price
    title = uploadContents.objects.get(contents_id=request.POST['id']).title
    selleraccount = Web3.toChecksumAddress(sellerinfo.account)
    buyerinfo = myPageInfomation.objects.get(email=request.session['user_email'])
    buyeraccount = Web3.toChecksumAddress(buyerinfo.account)
    buyerpwd = request.POST['pwd']
    print(buyerpwd)
    print(selleraccount)
    print(buyeraccount)
    print(price)
    w3.personal.unlockAccount(buyeraccount, buyerpwd, 0)
    tx_hash = ncc.functions.transfer(selleraccount, price).transact({'from': w3.eth.coinbase, 'gas': 2000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()

    contents_id = uploadContents.objects.get(contents_id=request.POST['id'])
    downloader_email = myPageInfomation.objects.get(email=request.session['user_email'])

    br = downloadContents (
                            contents_id=contents_id,
                            downloader_email=downloader_email

    )
    br.save()

    wif = walletInFormation (
                            fromAccount=buyerinfo.email,
                            toAccount=sellerinfo.email,
                            balance= price,
                            type="contentsTrasaction",
                            txid=receipt,
                            transactiondate=timezone.now(),
                            aaa=title
    )
    wif.save()


    res = {'Ans': '결제되었습니다.'}
    return JsonResponse(res)

def main(request):
    populated_informations = Post.objects.order_by('like_count')[0:6]

    populated_reports_lists = uploadContents.objects.order_by('downloadcount').filter(category="레포트")[0:6]
    populated_forlecture_lists = uploadContents.objects.order_by('downloadcount').filter(category="강의자료")[0:6]
    populated_note_lists = uploadContents.objects.order_by('downloadcount').filter(category="강의노트")[0:6]
    populated_fortest_lists = uploadContents.objects.order_by('downloadcount').filter(category="시험자료")[0:6]
    populated_video_lists = uploadContents.objects.order_by('downloadcount').filter(category="동영상")[0:6]
    populated_fiction_lists = uploadContents.objects.order_by('downloadcount').filter(category="자소서")[0:6]
    populated_resume_lists = uploadContents.objects.order_by('downloadcount').filter(category="이력서")[0:6]
    populated_PPT_lists = uploadContents.objects.order_by('downloadcount').filter(category="PPT")[0:6]
    populated_paper_lists = uploadContents.objects.order_by('downloadcount').filter(category="논문")[0:6]
    if request.session.keys():
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])

        return render(request, 'unid/contentstran.html', {
                                                            'populated_informations': populated_informations,

                                                            'populated_reports_lists': populated_reports_lists,
                                                            'populated_forlecture_lists': populated_forlecture_lists,
                                                            'populated_note_lists':populated_note_lists,
                                                            'populated_paper_lists': populated_paper_lists,
                                                            'populated_PPT_lists': populated_PPT_lists,
                                                            'populated_resume_lists': populated_resume_lists,
                                                            'populated_fiction_lists': populated_fiction_lists,
                                                            'populated_fortest_lists': populated_fortest_lists,
                                                            'populated_video_lists': populated_video_lists,
                                                            'mypage':mypage
                                                        })
    else :
        return render(request, 'unid/contentstran.html', {
            'populated_informations_school': populated_informations,

            'populated_reports_lists': populated_reports_lists,
            'populated_forlecture_lists': populated_forlecture_lists,
            'populated_note_lists': populated_note_lists,
            'populated_paper_lists': populated_paper_lists,
            'populated_PPT_lists': populated_PPT_lists,
            'populated_resume_lists': populated_resume_lists,
            'populated_fiction_lists': populated_fiction_lists,
            'populated_fortest_lists': populated_fortest_lists,
            'populated_video_lists': populated_video_lists
        })

def info_popular(request):
    if request.session.keys():
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        posts = Post.objects.order_by('-like_count', '-created_at')
        sess = request.session['user_email']
        voting_count = myPageInfomation.objects.get(email=sess)
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts}
            return render(request, 'unid/info_popular_ajax.html', context)

        context = {'posts':posts, 'voting_count':voting_count, 'mypage':mypage}

        return render(request, 'unid/info_popular.html', context)
    else:
        posts = Post.objects.order_by('-like_count', '-created_at')
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts}
            return render(request, 'unid/info_popular_ajax.html', context)

        context = {'posts': posts}

        return render(request, 'unid/info_popular.html', context)


def information(request):
    if request.session.keys():
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        posts = Post.objects.order_by('-posts_id')
        sess = request.session['user_email']
        voting_count = myPageInfomation.objects.get(email=sess)
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts}
            return render(request, 'unid/information_ajax.html', context)

        context = {'posts':posts, 'voting_count':voting_count, 'mypage':mypage}

        return render(request, 'unid/information.html', context)
    else:
        posts = Post.objects.order_by('-posts_id')
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts}
            return render(request, 'unid/information_ajax.html', context)

        context = {'posts': posts}

        return render(request, 'unid/information.html', context)

def vote(request):
    sess = request.session['user_email']
    posts_id = request.POST['posts_id']
    list = LikeUsers.objects.filter(posts_id=posts_id, liked_users=sess)
    count = myPageInfomation.objects.get(email=sess)
    voting_count = count.votingcount
    list = list.values()

    if list:
        if voting_count < 0:
            res = {"Ans": "보팅을 모두 소진하셨습니다."}
        else:
            res = {"Ans": "보팅을 취소했습니다."}
    else:
        if voting_count == 0:
            res = {"Ans": "보팅을 모두 소진하셨습니다."}
        else:
            res = {"Ans": "보팅을 완료했습니다."}

    return JsonResponse(res)

def my_cron_job(request):
    voting_count = request.POST['voting_count']
    myProfile = myPageInfomation.objects.all()

    for count in myProfile:
        count.votingcount = 10
        count.save()

    res = {"Ans": "보팅이 충전되었습니다."}

    return JsonResponse(res)

def main_detail(request, id):
    posts = Post.objects.get(posts_id=id)
    replys = replyForPosts.objects.filter(posts_id=id).values()
    likes = LikeUsers.objects.filter(posts_id=id)
    if request.session.keys():
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        context = {'posts': posts, 'replys': replys, 'likes':likes, 'mypage':mypage}
    else:
        context = {'posts': posts, 'replys': replys, 'likes': likes}
    return render(request, 'unid/main_detail.html', context)

def voting(request):
    posts_id=request.POST['posts_id']
    like_count=request.POST['like_count']
    rewards=request.POST['rewards']
    liked_users=request.POST['liked_users']
    votinged = request.POST['votinged']
    count = myPageInfomation.objects.get(email=liked_users)
    voting_count = count.votingcount


    if votinged=="좋아요취소":

        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.rewards = rewards
        count.votingcount = int(voting_count) + 1
        posts.save()
        count.save()

        posts_id = Post.objects.get(posts_id=posts_id)

        voting_delete = LikeUsers.objects.filter(posts_id=posts_id, liked_users=liked_users)

        for delete in voting_delete:
            delete.delete()

    elif votinged=="좋아요":
        count.votingcount = int(voting_count) -1
        count.save()
        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.rewards = rewards
        posts.save()

        posts_id = Post.objects.get(posts_id=posts_id)

        like = LikeUsers(posts_id=posts_id, liked_users=liked_users)

        like.save()
    else :
        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.rewards = rewards
        posts.save()


    url = '../'
    return HttpResponseRedirect(url)


def mainreply(request):

    id =Post.objects.get(posts_id=request.POST['id'])
    sess = request.session['user_email']
    user = myPageInfomation.objects.get(email=sess)
    br = replyForPosts(posts_id=id,
                           user=user,
                           replytext=request.POST['reply']
                           )

    br.save()

    res = {"Ans": "댓글 작성이 완료되었습니다."}
    return JsonResponse(res)

def main_upload(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(request, 'unid/main_upload.html', {'mypage':mypage})
    else:
        sess = request.session['user_email']
        title = request.POST['title']
        category = request.POST['category']
        contents = request.POST['contents']
        tags = request.POST['tags']
        upload_file = request.FILES['user_files']
        with open("unid/static/unid/img" + '/' + upload_file.name, 'wb') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        user = myPageInfomation.objects.get(email=sess)

        info = Post(title=title, user=user, category=category, contents=contents, file=upload_file.name, tags=tags)
        info.save()

        url = '/unid'
        return HttpResponseRedirect(url)


def login(request):
    return render(request, 'unid/login.html', {})


def signup(request):
    return render(request, 'unid/signup.html', {})

@login_required
def createaccount(request):
    if request.method == 'GET':
        account = myPageInfomation.objects.get(email=request.session['user_email']).account
        if account:
            request.session['user_account'] = account
            url = '/unid'
            return HttpResponseRedirect(url)
        else:
            return render(request, 'unid/createaccount.html', {})
    else:
        rpc_url = "http://222.239.231.252:9545"
        w3 = Web3(HTTPProvider(rpc_url))
        # return HttpResponse(w3.eth.accounts)

        kk = w3.personal.listAccounts
        print(kk)


        password = request.POST['pwd']
        account = w3.personal.newAccount(password)
        lockpwd = sha256(password.encode('utf-8'))

        myPageInfomation.objects.filter(email=request.session['user_email']).update(
                            joiningdate=timezone.now(),
                            pwd=lockpwd,
                            account=account
                            )
        url = '/unid'

        return HttpResponseRedirect(url)

@login_required
def contentsupload(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        return render(request, 'unid/contentsupload.html', {'mypage':mypage})
    else:  # submit으로 제출
        try:
            # upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
            # print(upload_files)
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError as e:
            pass
        # try:
        #     number = str(random.random())
        #     print(number)
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        #     os.mkdir("uploadfiles/" + number)  # 그 날짜에 맞는 디렉토리 생성
        # except FileExistsError as e:
        #     pass
        try:
            print(os.getcwd())
            os.mkdir("media/" + today)
        except FileExistsError as e:
            pass
        # print(2)
        # ftpfilelist = []
        # uifilelist = []
        # filehashdatas = []
        # filesize = []
        # contents_dir = "uploadfiles/" + number + "/"
        # for upload_file in upload_files:  # 다중 파일 업로드
        #     # file_name = upload_file.name
        #     # number = str(random.random())
        #     filename = upload_file.name
        #     extendname = filename[filename.find(".", -4):]
        #     # real_filename = number + extendname
        #     # ftpfilelist.append(real_filename)
        #     uifilelist.append(filename)
        #     # now = datetime.now()
        #     # today = now.strftime('%Y-%m-%d')
        #     # 해당 날짜의 디렉토리
        #     with open(contents_dir + filename, 'wb') as file:  # 저장경로
        #         for chunk in upload_file.chunks():
        #             file.write(chunk)
        #     with open(contents_dir + filename, 'rb') as file:
        #         filedata = file.read()
        #         hashdata = hashlib.sha256(filedata).hexdigest()
        #         filehashdatas.append(hashdata)
        #     file_size = os.path.getsize(contents_dir + filename)
        #     filesize.append(file_size)

        # if len(uifilelist) == 1:
        #     filename = uifilelist[0]
        #     print(filename)
        #     zipname = number + ".zip"
        #     password = filehashdatas[0][0:8]
        #     # with open(contents_dir + filename, 'wb') as file:
        #     pyminizip.compress_multiple([contents_dir + filename], ["Unid_Contents"], contents_dir + zipname, password,
        #                                 4)
        # elif len(uifilelist) == 2:
        #     filename = uifilelist[0]
        #     filename2 = uifilelist[1]
        #     zipname = number + ".zip"
        #     password = filehashdatas[0][0:8]
        #     pyminizip.compress_multiple([contents_dir + filename, contents_dir + filename2],
        #                                 ["Unid_Contents", "Unid_Contents"], contents_dir + zipname, password, 4)

        preview_save_filelist = []
        preview_ui_filelist = []
        for upload_image in upload_images:
            image_number = str(random.random())
            previewfilename = upload_image.name
            extendname = previewfilename[previewfilename.find(".", -5):]
            real_preview_filename = image_number + extendname
            preview_save_filelist.append(real_preview_filename)
            preview_ui_filelist.append(previewfilename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            print(os.getcwd())
            contents_dir = "media/" + today + "/"
            # 해당 날짜의 디렉토리
            with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                for chunk in upload_image.chunks():
                    file.write(chunk)
            im = Image.open(contents_dir + real_preview_filename)
            size = (1000, 1050)
            im2 = im.resize(size)
            im2.save(contents_dir + real_preview_filename)
        contents_dir = "media/" + today + "/"
        try:
            thumb = Image.open(contents_dir + preview_save_filelist[0])
            size = (180, 200)
            thumbnailimage = thumb.resize(size)
            thumbnailimage.save(contents_dir + "thumb" + preview_save_filelist[0])
        except IndexError as e:
            pass

        """

        검수시스템 추후 개발예정

        """
        print("fpt start")
        ftp = FTP()
        ftp.connect("222.239.231.253")  # Ftp 주소 Connect(주소 , 포트)
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd("/home/unid/contents")
        ftp_contents_dir = "/home/unid/contents/" + today + "/"
        print("fpt")
        try:
            ftp.mkd(today)
            print("fpt1")
        except:
            ftp.cwd("/home/unid/contents/" + today)
            print("fpt2")
        ftp.cwd("/home/unid/contents/" + today)
        print("fpt3")
        print(os.getcwd())
        filepath = request.POST['filepath']
        filename = request.POST['filename']

        print("fpt4")
        print(os.getcwd())
        os.chdir(filepath)
        print("fpt5")
        print(os.getcwd())
        # contents_dir = today + "/"
        # # with open(contents_dir + file_name, "wb") as file:
        # #     ftp.storlines('STOR %s' % file_name, file)

        uploadfile = open(filename, "rb")
        print("fpt6")
        print(os.getcwd())
        ftp.storbinary('STOR ' + filename, uploadfile)

        print("fpt end")
        uploadfile.close()
        print(os.getcwd())
        os.chdir("..")
        print(os.getcwd())
        os.chdir("..")
        print(os.getcwd())
        shutil.rmtree(filepath)
        print(os.getcwd())
        publisheddate = str(request.POST['publisheddate'])[0:10]
        preview_images_dir = "media/" + today + "/"
        writeremail = myPageInfomation.objects.get(email=request.session['user_email'])
        try:
            br = uploadContents(
                writeremail=writeremail,
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                # totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                downloadcount=0,
                replymentcount=0
            )
            br.save()
        except IndexError as e:
            br = uploadContents(
                writeremail=writeremail,
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                # totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                downloadcount=0,
                replymentcount=0
            )
            br.save()
        uifilelist = request.POST['uifilelist'].split(',')
        filehashdatas = request.POST['filehashdatas'].split(',')
        filesize = request.POST['filesize'].split(',')
        idx = uploadContents.objects.all().order_by('-pk')[0]  # ★
        filelistlength = len(filehashdatas)
        print(filelistlength)


        preview_images_dir = "media/" + today + "/"
        previewlistlength = len(preview_save_filelist)
        for i in range(previewlistlength):
            print(7)
            br = previewInfo(
                contents_id=idx,
                uploadpreviewname=preview_ui_filelist[i],
                savepreviewname=preview_save_filelist[i],
                imagepath=preview_images_dir + preview_save_filelist[i],
            )
            br.save()

        rpc_url = "http://222.239.231.252:9545"
        w3 = Web3(HTTPProvider(rpc_url))
        print("시작 트랜젝션")
        contentsMasterContract_address = Web3.toChecksumAddress("0x22862cf6b8c28aba4f0b519e3c93a31b9edd0d31")

        cmc = w3.eth.contract(address=contentsMasterContract_address, abi= [{"constant":False,"inputs":[{"name":"name","type":"string"},{"name":"hash","type":"string"}],"name":"addContents","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}])

        price = int(request.POST['price'])
        transactionHashList = []
        for i in range(len(filehashdatas)):
            # cmc.functions.addContents(request.session['user_email'], request.POST['price'], filehashdatas[i]).transact({"from": w3.eth.accounts[-4], "gas": 1000000 })
            tx_hash = cmc.functions.addContents(request.session['user_email'], filehashdatas[i]).transact(
                {"from": w3.eth.accounts[0], "gas": 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
            transactionHashList.append(receipt)

        for i in range(filelistlength):
            print(6)
            br = contentsInfo(
                contents_id=idx,
                uploadzipfilename=filename,
                uploadfile=uifilelist[i],
                contentspath=ftp_contents_dir,
                hash=filehashdatas[i],
                filesize=filesize[i],
                bbb=transactionHashList[i]
            )
            br.save()

        url = '/unid/searchcontents/'+ request.POST['category']
        return HttpResponseRedirect(url)

@csrf_exempt
def test_validfile(request):
    try:
        print(os.getcwd())
        upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
        print(upload_files)
    except MultiValueDictKeyError as e:
        pass
    try:
        number = str(random.random())
        print(number)
        print(os.getcwd())
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        print(os.getcwd())
        os.mkdir("uploadfiles/" + number)  # 그 날짜에 맞는 디렉토리 생성
        print(os.getcwd())
    except FileExistsError as e:
        pass
    try:
        print(os.getcwd())

        os.mkdir("media/" + today)
    except FileExistsError as e:
        pass
    print(2)
    ftpfilelist = []
    uifilelist = []
    filehashdatas = []
    filesize = []
    already_uploaded_list = []
    contents_dir = "uploadfiles/" + number + "/"
    for upload_file in upload_files:  # 다중 파일 업로드
        # file_name = upload_file.name
        # number = str(random.random())
        filename = upload_file.name
        extendname = filename[filename.find(".", -4):]
        # real_filename = number + extendname
        # ftpfilelist.append(real_filename)
        uifilelist.append(filename)
        # now = datetime.now()
        # today = now.strftime('%Y-%m-%d')
        # 해당 날짜의 디렉토리
        with open(contents_dir + filename, 'wb') as file:  # 저장경로
            for chunk in upload_file.chunks():
                file.write(chunk)
        with open(contents_dir + filename, 'rb') as file:
            filedata = file.read()
            hashdata = hashlib.sha256(filedata).hexdigest()
            filehashdatas.append(hashdata)

        if contentsInfo.objects.filter(hash=hashdata):
            print("똑같아")
            # shutil.rmtree("uploadfiles/" + number)
            already_uploaded_list.append(filename)

        file_size = os.path.getsize(contents_dir + filename)
        print(file_size)
        filesize.append(str(file_size/1000) + "KB")
    print("중복없음")
    # res = {"Ans": "해당 파일은 이미 등록 되어있습니다 : " + filename}
    # return JsonResponse(res)
    if already_uploaded_list:
        res = {"Ans": "해당 파일은 이미 등록 되어있습니다 : ",
               "list": already_uploaded_list }
        shutil.rmtree("uploadfiles/" + number)
        return JsonResponse(res)
    else:
        print(os.getcwd())
        os.chdir("uploadfiles/" + number)
        print(os.getcwd())


        with zipfile.ZipFile('Unid_contents' + number + '.zip', mode='w') as f:
            print(uifilelist[0])
            f.write(uifilelist[0], compress_type=zipfile.ZIP_DEFLATED)
        if len(uifilelist) >= 2:
            for i in range(len(uifilelist)-1):
                with zipfile.ZipFile('Unid_contents' + number + '.zip', mode='a') as f:
                    f.write(uifilelist[i+1], compress_type=zipfile.ZIP_DEFLATED)
        os.chdir("..")
        os.chdir("..")
        print(os.getcwd())
        res = {
                "Ans":"업로드 가능한 콘텐츠입니다.",
                "test":"test",
                "filepath": contents_dir,
                "filename": 'Unid_contents' + number + '.zip',
                "ftpfilelist": ftpfilelist,
                "uifilelist": uifilelist,
                "filehashdatas": filehashdatas,
                "filehashdata": filehashdatas[0],
                "filesize": filesize
        }

        return_obj = JsonResponse(res)
        return return_obj

@login_required
def postmodify(request, id):
    if request.method == 'GET':
        contents = uploadContents.objects.get(contents_id=id)
        contentsinfolist = []
        for i in range(len(contentsInfo.objects.filter(contents_id=id).values())):
            contentsinfolist.append(contentsInfo.objects.filter(contents_id=id).values()[i]['uploadzipfilename'])
        publisheddate = str(contents.publisheddate)[0:10]

        return render(request, 'unid/postmodify.html', {'contents': contents, 'date':publisheddate, 'contentsinfolist': contentsinfolist})
    else:

        try:
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError:
            pass
        if upload_images:
            for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
                previewfilepath = previewInfo.objects.filter(contents_id=id).values()[i]['imagepath']
                print(os.getcwd())
                os.remove(previewfilepath)
            thumbnailimagepath = uploadContents.objects.get(contents_id=id).imagepath
            os.remove(thumbnailimagepath)
            previewInfo.objects.filter(contents_id=id).delete()
            try:
                now = datetime.now()
                today = now.strftime('%Y-%m-%d')
                print(os.getcwd())
                os.mkdir("media/" + today)
            except FileExistsError as e:
                pass

            preview_save_filelist = []
            preview_ui_filelist = []
            for upload_image in upload_images:
                image_number = str(random.random())
                previewfilename = upload_image.name
                extendname = previewfilename[previewfilename.find(".", -5):]
                real_preview_filename = image_number + extendname
                preview_save_filelist.append(real_preview_filename)
                preview_ui_filelist.append(previewfilename)
                now = datetime.now()
                today = now.strftime('%Y-%m-%d')
                print(os.getcwd())
                contents_dir = "media/" + today + "/"
                # 해당 날짜의 디렉토리
                with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                    for chunk in upload_image.chunks():
                        file.write(chunk)
                im = Image.open(contents_dir + real_preview_filename)
                size = (1000, 1050)
                im2 = im.resize(size)
                im2.save(contents_dir + real_preview_filename)
            try:
                thumb = Image.open(contents_dir + preview_save_filelist[0])
                size = (180, 200)
                thumbnailimage = thumb.resize(size)
                thumbnailimage.save(contents_dir + "thumb" + preview_save_filelist[0])
            except IndexError as e:
                pass

            preview_images_dir = "media/" + today + "/"
            previewlistlength = len(preview_save_filelist)
            for i in range(previewlistlength):
                print(7)
                br = previewInfo(
                    contents_id=id,
                    uploadpreviewname=preview_ui_filelist[i],
                    savepreviewname=preview_save_filelist[i],
                    imagepath=preview_images_dir + preview_save_filelist[i],
                )
                br.save()

            uploadContents.objects.filter(contents_id=id).update(
                title=request.POST['title'],
                publisheddate=str(request.POST['publisheddate'])[0:10],
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                # totalpages=request.POST['totalpages'],
                imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                last_modified=timezone.now()
            )
        uploadContents.objects.filter(contents_id=id).update(
            title=request.POST['title'],
            publisheddate=str(request.POST['publisheddate'])[0:10],
            category=request.POST['category'],
            price=request.POST['price'],
            tags=request.POST['tags'],
            # totalpages=request.POST['totalpages'],
            authorinfo=request.POST['authorinfo'],
            intro=request.POST['intro'],
            index=request.POST['index'],
            contents=request.POST['contents'],  # 소개글 제한?
            reference=request.POST['reference'],
            last_modified=timezone.now()
        )

        url = '/unid/searchcontents/'+request.POST['category']
        return HttpResponseRedirect(url)

@login_required
def postdelete(request):
    uploadContents.objects.filter(contents_id=request.POST['id']).update(
        last_modified=timezone.now(),
        isdelete="삭제"
    )

    res = {"Ans": "삭제되었습니다."}
    return JsonResponse(res)

@login_required
def download(request):
    if request.method == "GET":
        id = request.GET['id']
        print(id)
        contentsfile = contentsInfo.objects.filter(contents_id=id).values()
        print(contentsfile)
        filepath = contentsfile[0]['contentspath']
        filename = contentsfile[0]['uploadzipfilename']
        print(filepath)
        print(filename)
        number = str(random.random())
        print(number)
        os.mkdir("downloads/" + number)
        ftp = FTP()
        ftp.connect("222.239.231.253")
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd(filepath)
        # downloadedfilename = contentsInfo.objects.filter(contents_id=id).values()['uploadzipfilename']
        fd = open(os.path.join(settings.BASE_DIR, 'downloads', number, filename), 'wb')
        ftp.retrbinary("RETR " + filename, fd.write)
        fd.close()

        filepath1 = os.path.join(settings.BASE_DIR, 'downloads', number, filename)
        print(filepath1)
        filename1 = os.path.basename(filepath1)
        print(filename1)

        board = uploadContents.objects.get(contents_id=id)
        board.downloadcount = board.downloadcount + 1
        board.save()

        # downloadid = request.GET['downloadid']
        with open(filepath1, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            # response['Set-Cookie'] = 'download=' + downloadid;
            response['Content-Disposition'] = 'attachment; filename="{}"'.format("Unid.zip")
            return response
@login_required
def writereply(request):
    id = uploadContents.objects.get(contents_id=request.POST['id'])
    writeremail = myPageInfomation.objects.get(email=request.session['user_email'])
    br = replysForContents(contents_id=id,
                           writeremail=writeremail,
                           replytext=request.POST['reply']
                           )

    br.save()
    board = uploadContents.objects.get(contents_id=request.POST['id'])
    board.replymentcount = board.replymentcount + 1
    board.save()
    created = replysForContents.objects.order_by('-contents_id').filter(contents_id=id).values()[0]['created']

    res = {
        "Ans": "댓글 작성이 완료되었습니다.",
        "writeremail": writeremail.email,
        "created": created,
        "replytext": request.POST['reply']
       }
    return JsonResponse(res)


def postview(request, id):  # GET 방식으로 입력박을 시 넘어오는 id. urls.py 에서도 path에 입력해줘야함.
    board = uploadContents.objects.get(contents_id=id)  # id에 해당하는 정보들
    board.hits = board.hits + 1    # 조회수 증가
    board.save()
    # id 에 해당하는 정보들을 html에 넘겨줘서 사용
    # viewwork.html 에서 {{ board.memo }} 로 내용물 확인 가능
    return render(request, 'unid/contentsdetail.html', {'board': board})


def searchcontents(request, category):
    allcontentslists = uploadContents.objects.order_by('-contents_id').filter(
                                            Q(category=category) & Q(isdelete__isnull=True)
                                        )
    return render(
        request, 'unid/searchcontents.html',
        {'contentslists': allcontentslists}
    )

@login_required
def opinion(request):

    br = opinions (
        posts_id = request.POST['id'],
        context = request.POST['category'],
        fromuser = request.session['user_email'],
        writeruser = request.POST['writeremail'],
        exceptopinion = request.POST['exceptOpinion'],
        bbb = request.POST['title'],
        ccc=  request.POST['type']
    )
    br.save()

    res = {'Ans': '소중한 의견 감사합니다.'}
    return JsonResponse(res)
def unidAdmin(request):
    allUsers = myPageInfomation.objects.all()
    allBlackList = blackList.objects.all()
    allTransacts = walletInFormation.objects.all()
    allContents = uploadContents.objects.all()
    allPost = Post.objects.all()
    allOpinions = opinions.objects.all()
    return render(request, 'unid/Unid_admin.html', {
                                                    'allUsers': allUsers,
                                                    'allBlackList': allBlackList,
                                                    'allTransacts': allTransacts,
                                                    'allContents': allContents,
                                                    'allPost': allPost,
                                                    'allOpinions': allOpinions
    })


def warninguser(request):
    id = request.POST['id']
    postType = request.POST['postType']
    writerUser = request.POST['writerUser']
    if postType == "contents":
        contents_info = uploadContents.objects.filter(contents_id=id)
        contents_info.update(isdelete="삭제")
        print(1)
        warningUser = myPageInfomation.objects.get(email=writerUser)
        print(2)
        print(warningUser)
        br = reasonForBan (
            user_id=warningUser,
            reason=request.POST['reason']
        )
        br.save()
        print(3)
        warningCount = len(reasonForBan.objects.filter(contents_id=id).values())
        print(4)
        print(warningCount)
        if warningCount == 3:
            br = blackList (
                user=warningUser
            )
            br.save()
            res = {'Ans': "경고 3회 누적: " + warningUser + "는(은) 블랙리스트 처리되었습니다"}
            return JsonResponse(res)
    else:
        information_info = Post.objects.filter(post_id=id)
        information_info.update(isdelete="삭제")
        warningUser = myPageInfomation.objects.get(email=writerUser)
        br = reasonForBan(
            user_id=warningUser,
            reason=request.POST['reason']
        )
        br.save()
        warningCount = len(reasonForBan.objects.filter(contents_id=id).values())
        if warningCount == 3:
            br = blackList(
                user=warningUser
            )
            br.save()
            res = {'Ans': "경고 3회 누적: " + warningUser + "는(은) 블랙리스트 처리되었습니다"}
            return JsonResponse(res)



def testpage(request):

    return render(request, 'unid/testpage.html', {})


def contentsBlockTest(request):
    rpc_url = "http://222.239.231.252:9545"
    w3 = Web3(HTTPProvider(rpc_url))
    print("시작 트랜젝션")
    contentsMasterContract_address = Web3.toChecksumAddress("0x22862cf6b8c28aba4f0b519e3c93a31b9edd0d31")

    cmc = w3.eth.contract(address=contentsMasterContract_address, abi=[
        {"constant": False, "inputs": [{"name": "name", "type": "string"}, {"name": "hash", "type": "string"}],
         "name": "addContents", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "contents",
         "outputs": [{"name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "getContentsAddressList",
         "outputs": [{"name": "contentsAddressList", "type": "address[]"}], "payable": False, "stateMutability": "view",
         "type": "function"}, {"anonymous": False, "inputs": [{"indexed": False, "name": "name", "type": "string"}],
                               "name": "EventAddContents", "type": "event"}])

    filehashdatas = request.POST['filehashdatas']

    tx_hash = cmc.functions.addContents("testID", filehashdatas).transact(
        {"from": w3.eth.accounts[0], "gas": 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
    transactionHashList= receipt


    res = {'Ans':'처리되었습니다.', 'receipt': transactionHashList}
    return JsonResponse(res)