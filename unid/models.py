from django.db import models
from django import forms
from datetime import datetime

from unidweb import settings


class myPageInfomation(models.Model):
    apiprovider = models.CharField(max_length=50, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=50, blank=True, null=True)
    userimage = models.CharField(max_length=200, blank=True, null=True)
    profile = models.CharField(max_length=200, blank=True, null=True)
    joiningdate = models.DateTimeField(null=True)
    votingcount = models.IntegerField(default=10)
    pwd = models.CharField(max_length=200, blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)
    like = models.IntegerField(null=True)
    downloadedcontents = models.CharField(max_length=250, blank=True, null=True)
    is_blacklist = models.CharField(max_length=10, blank=True, null=True)
    blacklist_count = models.IntegerField(blank=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)
    ddd = models.CharField(max_length=250, blank=True, null=True)

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

class uploadContents(models.Model):
    contents_id = models.AutoField(primary_key=True)
    writeremail = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publisheddate = models.DateTimeField(null=True)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    tags = models.CharField(max_length=50)
    fileinfo = models.CharField(max_length=250)
    # totalpages = models.IntegerField()
    authorinfo = models.CharField(max_length=1000)
    intro = models.CharField(max_length=1000)
    index = models.CharField(max_length=1000)
    contents = models.CharField(max_length=1000)  # 소개글 제한?
    reference = models.CharField(max_length=1000, default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    downloadcount = models.IntegerField(null=True)
    isdelete = models.CharField(max_length=10, null=True)
    imagepath = models.CharField(max_length=200, null=True)
    hits = models.IntegerField(default=0)
    txid = models.CharField(max_length=250, blank=True, null=True)
    replymentcount = models.IntegerField(null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)
    ddd = models.CharField(max_length=250, blank=True, null=True)

class downloadContents(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.ForeignKey(uploadContents, on_delete=models.CASCADE)
    downloader_email = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)


class contentsInfo(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.ForeignKey(uploadContents, on_delete=models.CASCADE)
    uploadzipfilename = models.CharField(max_length=100)
    uploadfile = models.CharField(max_length=100, null=True)
    contentspath = models.CharField(max_length=200)
    hash = models.CharField(max_length=150, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    filesize = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class previewInfo(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.ForeignKey(uploadContents, on_delete=models.CASCADE)
    uploadpreviewname = models.CharField(max_length=100)
    savepreviewname = models.CharField(max_length=100)
    imagepath = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class replysForContents(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.ForeignKey(uploadContents, on_delete=models.CASCADE)
    writeremail = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    replytext = models.CharField(max_length=1000, blank=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class walletInFormation(models.Model):
    IDX=models.AutoField(primary_key=True)
    transactiondate = models.DateTimeField(null=True, editable=False)
    fromAccount = models.CharField(max_length=100, blank=True, null=True, editable=False)
    toAccount = models.CharField(max_length=100, blank=True, null=True, editable=False)
    balance = models.IntegerField(blank=True, null=True, editable=False)
    txid = models.CharField(max_length=100, blank=True, null=True, editable=False)
    type = models.CharField(max_length=100, blank=True, null=True, editable=False)
    user = models.CharField(max_length=100, blank=True, null=True, editable=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)


class blackList(models.Model):
    IDX = models.AutoField(primary_key=True)
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    is_blacklist = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    count = models.IntegerField()
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class reasonForBan(models.Model):
    IDX = models.AutoField(primary_key=True)
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    reason = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class superUser(models.Model):
    IDX = models.AutoField(primary_key=True)
    log = models.CharField(max_length=50)
    reason_for_modify = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class adBySuperUser(models.Model):
    IDX = models.AutoField(primary_key=True)
    advertiser = models.CharField(max_length=100)
    ad_path = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class Post(models.Model):
    posts_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    file = models.FileField(max_length=1000, null=True)
    file_path = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=1000, help_text="내용을 작성해주세요")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=100)
    rewards = models.FloatField(default=0)
    liked_users = models.CharField(max_length=50)
    like_count = models.IntegerField(default=0)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    isdelete = models.CharField(max_length=250, blank=True, null=True)

class LikeUsers(models.Model):
    IDX = models.AutoField(primary_key=True)
    liked_users = models.CharField(max_length=100)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class replyForPosts(models.Model):
    IDX = models.AutoField(primary_key=True)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    replytext = models.CharField(max_length=1000, blank=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class opinions(models.Model):
    IDX = models.AutoField(primary_key=True)
    posts_id = models.IntegerField()
    context = models.CharField(max_length=100)
    fromuser = models.CharField(max_length=100)
    writeruser = models.CharField(max_length=100)
    exceptopinion = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)
