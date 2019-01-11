import os
from _sha256 import sha256
from datetime import datetime
from ftplib import FTP
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST
from web3 import Web3, HTTPProvider
from django.shortcuts import render
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from .models import *
import random
from django.shortcuts import render
import hashlib


def mypage(request):
    # mypage = MypageInfomation.objects.get(email)
    contentsboard = uploadContents.objects.all()
    context = {'mypage': mypage,
               'contentsboard': contentsboard}
    return render(request, 'unid/mypage.html', context)


def contentsboard(request):
    contentsboard = uploadContents.objects.all()
    context = {'contentsboard': contentsboard}
    return render(request, 'unid/contentsboard.html', context)


def mywallet(request):
    walletInfo = walletInFormation.objects.all()
    walletcount = walletInFormation.objects.count()
    # html = ''
    # for info in walletInfo:
    #     info.transactiondate = timezone.now()
    #     html += str(info.transactiondate) + '<br>' + info.fromAccount + '<br>' +info.toAccount + '<br>'+ str(info.balance) + '<br>'+ info.txid
    return render(request,'unid/mywallet.html', {'list':walletInfo, 'count':walletcount})


def transaction(request):
    if request.method == 'GET':
        return render(request, 'unid/transaction.html', {})
    else:
        from_account = request.POST['from_account']
        to_account = request.POST['to_account']
        account_bal = request.POST['account_bal']
        tran_id = request.POST['tran_id']

        transactionData = walletInFormation(fromAccount=from_account, toAccount=to_account, balance=account_bal, txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("transaction")
        transactionData.save()

    return render(request,'unid/transaction.html', {})

def exchange(request):
    return  render(request, 'unid/exchange.html', {})

def purchase(request):
    return  render(request, 'unid/purchase.html', {})

def contentsdetail(request, id):
    contents = uploadContents.objects.get(contents_id=id)
    replys = replysForContents.objects.filter(contents_id=id).values()

    # date = contents.created
    # print(date[0:4])

    # preview = previewInfo.objects.get(contents_id=id)
    # return HttpResponse(contents.title)
    return render(
        request,
        'unid/contentsdetail.html',
        {'contents': contents, 'replys': replys}
        # , 'preview': preview}
    )


def contentstran(request):
    return render(request, 'unid/contentstran.html', {})


def main(request):
    posts=Post.objects.order_by('-posts_id')
    votes= Voting.objects.all()
    context = {'posts': posts}
    return render(request, 'unid/main.html', context)

def main_detail(request, id):
    posts = Post.objects.get(posts_id=id)
    replys = replyForPosts.objects.filter(posts_id=id).values()

    return render(request, 'unid/main_detail.html', {'posts': posts, 'replys': replys})

def mainreply(request):
    br = replyForPosts(posts_id=request.POST['id'],
                           user=request.session['user_email'],
                           replytext=request.POST['reply']
                           )

    br.save()

    res = {"Ans": "댓글 작성이 완료되었습니다."}
    return JsonResponse(res)

def voting(request):
    vr = Voting(posts_id=request.POST['posts_id'],
                voting_count=request.POST['voting'],
                    )
    vr.save()

    res = {"Ans": "보팅이 완료되었습니다."}
    return JsonResponse(res)





def main_upload(request):
    if request.method == 'GET':
        return render(request, 'unid/main_upload.html', {})
    else:
        sess = request.session['user_email']
        title = request.POST['title']
        category = request.POST['category']
        contents = request.POST['contents']
        upload_file = request.FILES['user_files']
        with open("unid/static/unid/img" + '/' + upload_file.name, 'wb') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        user = myPageInfomation.objects.get(email=sess)

        info = Post(user=user, title=title, category=category, contents=contents, file=upload_file.name)
        info.save()

        url = '../unid/'
        return HttpResponseRedirect(url)


def login(request):
    return render(request, 'unid/login.html', {})


def signup(request):
    return render(request, 'unid/signup.html', {})


def createaccount(request):
    if request.method == 'GET':
        return render(request, 'unid/createaccount.html', {})
    else:
        rpc_url = "http://localhost:8545"
        w3 = Web3(HTTPProvider(rpc_url))

        pwd = request.POST['pwd']
        account = w3.personal.newAccount(pwd)
        br = myPageInfomation(email=request.POST['email'],
                              name=request.POST['name'],
                              joiningdate=timezone.now(),
                              pwd=request.POST['pwd'],
                              account=account
                              )
        br.save()
        url = 'http://localhost:8000/unid'
        return HttpResponseRedirect(url)


def oauth(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code&client_id=122f531f95d70dabb69ff17f4f1b0be2&redirect_uri=http://localhost:8000/unid/oauth&code=" + str(
            code)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        # response는 json형식이 아니니까 밑에 코드를 통해 json형식으로 바꾼다
        access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        # return  HttpResponse(access_token)
        url = "https://kapi.kakao.com/v1/user/signup"
        headers.update({'Authorization': "Bearer " + str(access_token)})
        response = requests.request("POST", url, headers=headers)
        # return HttpResponse(response.text)
        url = "https://kapi.kakao.com/v1/user/me"
        response = requests.request("POST", url, headers=headers)
        # email = json.loads(((response.text).encode('utf-8')))['email']
        id = json.loads(((response.text).encode('utf-8')))['id']
        nickname = json.loads(((response.text).encode('utf-8')))['properties']['nickname']
        try:
            member = myPageInfomation.objects.get(email=id)
        except myPageInfomation.DoesNotExist:
            return render(
                request,
                'unid/createaccount.html',
                {'id': id, 'nickname': nickname}
            )
        else:
            request.session['user_email'] = member.email
            request.session['user_name'] = member.name
            request.session['user_account'] = member.account

            url = 'http://localhost:8000/unid/mywallet'
            return HttpResponseRedirect(url)

    else:
        time = timezone.now()
        rpc_url = "http://localhost:8545"
        w3 = Web3(HTTPProvider(rpc_url))

        password = request.POST['pwd']  # ★★★★
        account = w3.personal.newAccount(password)
        lockpwd = sha256(password.encode('utf-8'))
        br = myPageInfomation(email=request.POST['email'],
                              name=request.POST['name'],
                              joiningdate=timezone.now(),
                              pwd=lockpwd,  # ★★★★
                              account=account)
        br.save()
        url = 'http://localhost:8000/unid'
        return HttpResponseRedirect(url)


def contentsupload(request):
    if request.method == 'GET':
        return render(request, 'unid/contentsupload.html', {})
    else:  # submit으로 제출
        try:
            upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
            upload_images = request.FILES.getlist('file_images')
        except MultiValueDictKeyError:
            pass
        try:
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            os.mkdir("uploadfiles/" + today)  # 그 날짜에 맞는 디렉토리 생성
            # root_dir = "우리 서버"   # ★★★★★★★★★★★
            # contents_dir = root_dir + "/" + today + "/"
            # contents_dir = today + "/"
        except FileExistsError as e:
            pass

        ftpfilelist = []
        uifilelist = []
        for upload_file in upload_files:  # 다중 파일 업로드
            # file_name = upload_file.name
            number = str(random.random())
            filename = upload_file.name
            extendname = filename[filename.find(".", -5):]
            real_filename = number + extendname
            ftpfilelist.append(real_filename)
            uifilelist.append(filename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            contents_dir = "uploadfiles/" + today + "/"
            # 해당 날짜의 디렉토리
            with open(contents_dir + real_filename, 'wb') as file:  # 저장경로
                for chunk in upload_file.chunks():
                    file.write(chunk)

        preview_ftp_filelist = []
        preview_ui_filelist = []
        for upload_image in upload_images:
            number = str(random.random())
            previewfilename = upload_image.name
            extendname = previewfilename[previewfilename.find(".", -5):]
            real_preview_filename = number + extendname
            preview_ftp_filelist.append(real_preview_filename)
            preview_ui_filelist.append(previewfilename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            contents_dir = "uploadfiles/" + today + "/"
            # 해당 날짜의 디렉토리
            with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                for chunk in upload_image.chunks():
                    file.write(chunk)

        # 검수시스템 추후 개발예정
        # session = ftplib.FTP('210.107.78.157')
        ftp = FTP()
        ftp.connect("210.107.78.157")  # Ftp 주소 Connect(주소 , 포트)
        ftp.login("unid", "dkagh")
        ftp.cwd("/home/unid/contents")
        ftp_contents_dir = "/home/unid/contents/" + today + "/"
        try:
            ftp.mkd(today)
        except:
            ftp.cwd("/home/unid/contents/" + today)
        ftp.cwd("/home/unid/contents/" + today)
        os.chdir("uploadfiles/" + today)
        # contents_dir = today + "/"
        # # with open(contents_dir + file_name, "wb") as file:
        # #     ftp.storlines('STOR %s' % file_name, file)

        filehashdatas = []
        for filename in ftpfilelist:
            file_name = filename
            uploadfile = open(file_name, "rb")
            ftp.storbinary('STOR ' + file_name, uploadfile)
            filedata = uploadfile.read()
            hashdata = hashlib.sha256(filedata).hexdigest()
            filehashdatas.append(hashdata)
            uploadfile.close()

        # Uploading preview file in preview folder
        ftp.cwd("/home/unid/images/contents")
        ftp_preview_images_dir = "/home/unid/images/contents/" + today + "/"
        try:
            ftp.mkd(today)
        except:
            ftp.cwd("/home/unid/images/contents/" + today)
        ftp.cwd("/home/unid/images/contents/" + today)
        for filename in preview_ftp_filelist:
            file_name = filename
            uploadfile = open(file_name, "rb")
            ftp.storbinary('STOR ' + file_name, uploadfile)
            uploadfile.close()
        os.chdir("..")
        os.chdir("..")
        br = uploadContents(
            writeremail=request.session['user_email'],
            title=request.POST['title'],
            publisheddate=request.POST['publisheddate'],
            category=request.POST['category'],
            price=request.POST['price'],
            tags=request.POST['tags'],
            fileinfo=request.POST['fileinfo'],
            totalpages=request.POST['totalpages'],
            # previewpath=request.POST['previewpath'],
            authorinfo=request.POST['authorinfo'],
            intro=request.POST['intro'],
            index=request.POST['index'],
            contents=request.POST['contents'],  # 소개글 제한?
            reference=request.POST['reference'],
        )
        br.save()

        idx = uploadContents.objects.all().order_by('-pk')[0].contents_id  # ★
        filelistlength = len(ftpfilelist)
        for i in range(filelistlength):
            br = contentsInfo(
                contents_id=idx,
                uploadfilename=uifilelist[i],
                ftpsavefilename=ftpfilelist[i],
                contentspath=ftp_contents_dir,
                hash=filehashdatas[i],
            )
            br.save()

        previewlistlength = len(preview_ftp_filelist)
        for i in range(previewlistlength):
            br = previewInfo(
                contents_id=idx,
                uploadpreviewname=preview_ui_filelist[i],
                ftpsavepreviewname=preview_ftp_filelist[i],
                imagepath=ftp_preview_images_dir,
            )
            br.save()

        rpc_url = "http://localhost:8545"
        w3 = Web3(HTTPProvider(rpc_url))

        contentsMasterContract_address = Web3.toChecksumAddress("0xa083498c49c29719887b040f003a714684ec4f4c")
        cmc = w3.eth.contract(address = contentsMasterContract_address, abi = [{"constant":False,"inputs":[{"name":"name","type":"string"},{"name":"price","type":"uint32"},{"name":"hash","type":"string"}],"name":"addContents","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}])
        w3.personal.unlockAccount(w3.eth.accounts[0], "pass0", 0)
        price = int(request.POST['price'])
        for i in range(len(filehashdatas)):
            # cmc.functions.addContents(request.session['user_email'], request.POST['price'], filehashdatas[i]).transact({"from": w3.eth.accounts[-4], "gas": 1000000 })
            cmc.functions.addContents(request.session['user_email'], price, filehashdatas[i]).transact({"from": w3.eth.accounts[0], "gas": 1000000 })

        url = '/unid/contentstran/'
        return HttpResponseRedirect(url)


@require_POST
def moneytrade(request):
    rpc_url = "http://localhost:8545"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0xa2b4fb8d101921540ea7f8dff906d1df07aa721d")
    ncc = w3.eth.contract(address = nidCoinContract_address, abi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])


    writeremail = request.POST['writeremail']
    sellerinfo = myPageInfomation.objects.get(email=writeremail)
    price = uploadContents.objects.get(contents_id=request.POST['id']).price
    selleraccount = Web3.toChecksumAddress(sellerinfo.account)
    buyeraccount = Web3.toChecksumAddress(request.session['user_account'])
    buyerpwd = request.POST['pwd']
    print(buyerpwd)
    print(selleraccount)
    print(buyeraccount)
    print(price)
    w3.personal.unlockAccount(buyeraccount, buyerpwd, 0)
    ncc.functions.transfer(selleraccount, price).transact({'from': buyeraccount, 'gas': 2000000})
    res = {'Ans': '결제되었습니다.'}
    return JsonResponse(res)
    # 거래 내역 디비에 담기


@require_POST
def download(request):
    id = request.POST['id']
    contentsinfos = contentsInfo.objects.filter(contents_id=id).values()
    fileplace = contentsinfos[0]['contentspath']
    print(contentsinfos)
    print(fileplace)
    ftp = FTP()
    ftp.connect("210.107.78.157")
    ftp.login("unid", "dkagh")
    ftp.cwd(fileplace)
    for i in range(len(contentsinfos)):
        filename = contentsinfos[i]['ftpsavefilename']
        fd = open(filename, 'wb')  # 다운로드 위치 ..
        ftp.retrbinary("RETR " + filename, fd.write)
    # 파일 이름 바꾸기...
    fd.close()
    # board = uploadContents.objects.get(contents_id=id)
    # board.downloadcount = board.downloadcount + 1
    # board.save()

    res = {'Ans': '다운로드 되었습니다.'}
    return JsonResponse(res)


#      filepath = os.path.join(settings.BASE_DIR, 'In/11_06_맛있는부산_데이터.db')
#      filename = os.path.basename(filepath)
#      with open(filepath, 'rb') as f:
#          response = HttpResponse(f, content_type='application/octet-stream')
#          response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
#          return response


def writereply(request):
    br = replysForContents(contents_id=request.POST['id'],
                           writeremail=request.session['user_email'],
                           replytext=request.POST['reply']
                           )

    br.save()

    res = {"Ans": "댓글 작성이 완료되었습니다."}
    return JsonResponse(res)


def postview(request, id):  # GET 방식으로 입력박을 시 넘어오는 id. urls.py 에서도 path에 입력해줘야함.
    board = uploadContents.objects.get(contents_id=id)  # id에 해당하는 정보들
    # board.hits = board.hits + 1    # 조회수 증가
    # board.save()
    # id 에 해당하는 정보들을 html에 넘겨줘서 사용
    # viewwork.html 에서 {{ board.memo }} 로 내용물 확인 가능
    return render(request, 'unid/contentsdetail.html', {'board': board})


def searchcontents(request, category):
    allcontentslists = uploadContents.objects.order_by('-contents_id').filter(category=category)
    # return HttpResponse(contentslists)
    return render(
        request, 'unid/searchcontents.html',
        {'contentslists': allcontentslists}
    )