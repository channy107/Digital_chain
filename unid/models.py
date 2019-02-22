from allauth.socialaccount.fields import JSONField
from django.db import models
from django import forms
from datetime import datetime


from unidweb import settings



class myPageInfomation(models.Model):
    IDX = models.IntegerField(null=True)
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

class richtextTest(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    delta_content = JSONField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def publish(self):
        self.published = True

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

class contentsnouns(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_nouns = models.CharField(max_length=10000, blank=True, null=True)
    contents_id = models.CharField(max_length=300, blank=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)


class uploadContents(models.Model):
    contents_id = models.AutoField(primary_key=True)
    writeremail = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publisheddate = models.DateTimeField(null=True)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    tags = models.CharField(max_length=50)
    fileinfo = models.CharField(max_length=250)
    authorinfo = models.CharField(max_length=1000)
    intro = models.CharField(max_length=2000)
    index = models.CharField(max_length=2000)
    checksimilar = models.CharField(max_length=50, null=True, blank=True)
    contents = models.CharField(max_length=2000)  # 소개글 제한?
    reference = models.CharField(max_length=2000, default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    downloadcount = models.IntegerField(null=True)
    isdelete = models.CharField(max_length=10, null=True)
    imagepath = models.CharField(max_length=200, null=True)
    hits = models.IntegerField(default=0)
    txid = models.CharField(max_length=250, blank=True, null=True)
    replymentcount = models.IntegerField(null=True)
    cagegory_path = models.CharField(max_length=250, blank=True, null=True)
    writername = models.CharField(max_length=50, blank=True, null=True)

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

class Post(models.Model):
    posts_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE, null=True)
    image_path = models.CharField(max_length=250, null=True)
    title = models.CharField(max_length=100)
    contents = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=100)
    rewards = models.FloatField(default=0)
    rewards_success = models.CharField(max_length=250, blank=True, null=True)
    like_count = models.IntegerField(default=0)
    writer_rewards = models.CharField(max_length=100, blank=True, null=True)
    category_path = models.CharField(max_length=250, blank=True, null=True)
    isdelete = models.CharField(max_length=250, blank=True, null=True)
    reward_date = models.DateTimeField(blank=True, null=True)
    replymentcount = models.IntegerField(default=0, null=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='LikeUsers')
    aaa = models.CharField(max_length=10000, blank=True, null=True)
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
    fromAccount = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE, null=True, related_name='fromAccount')
    toAccount = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE, null=True, related_name='toAccount')
    balance = models.FloatField(blank=True, null=True, editable=False)
    txid = models.CharField(max_length=100, blank=True, null=True, editable=False)
    type = models.CharField(max_length=100, blank=True, null=True, editable=False)
    user = models.CharField(max_length=100, blank=True, null=True, editable=False)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    contents_id = models.ForeignKey(uploadContents, on_delete=models.CASCADE, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)


class unidBlackList(models.Model):
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    IDX = models.AutoField(primary_key=True)
    is_blacklist = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    count = models.IntegerField()
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class blackReasonForBan(models.Model):
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    IDX = models.AutoField(primary_key=True)
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




class postImage(models.Model):
    IDX = models.AutoField(primary_key=True)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    uploadfilename = models.CharField(max_length=100)
    imagepath = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class LikeUsers(models.Model):
    IDX = models.AutoField(primary_key=True)
    liked_users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE, null=True)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    rewards_success = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        unique_together = (
            ('liked_users', 'posts_id')
        )

class replyForPosts(models.Model):
    IDX = models.AutoField(primary_key=True)
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE, null=True)
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
    title = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)


class advertise(models.Model):
    IDX = models.AutoField(primary_key=True)
    company = models.CharField(max_length=250)
    image_path = models.CharField(max_length=250)
    advertiser = models.CharField(max_length=250)
    startdate = models.CharField(max_length=250, blank=True, null=True)
    enddate = models.CharField(max_length=250, blank=True, null=True)
    price = models.CharField(max_length=250, blank=True, null=True)
    introduce = models.CharField(max_length=250, blank=True, null=True)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class adBySuperUser(models.Model):
    IDX = models.AutoField(primary_key=True)
    ad_id = models.ForeignKey(advertise, on_delete=models.CASCADE, null=True)
    adname = models.CharField(max_length=100)
    ad_path = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    aaa = models.CharField(max_length=250, blank=True, null=True)
    bbb = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)

class fundPost(models.Model):
    IDX = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    context = models.CharField(max_length=250)
    targetAmount = models.IntegerField()
    currentAmount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    expireDate = models.CharField(max_length=250, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    funderEmail = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    tags = models.CharField(max_length=250)
    sharePeopleNumber = models.IntegerField()
    isfunding = models.CharField(max_length=250, blank=True, null=True)
    fundCategory = models.CharField(max_length=250, blank=True, null=True)
    ccc = models.CharField(max_length=250, blank=True, null=True)
    fundaccount = models.CharField(max_length=250, blank=True, null=True)
    txid = models.CharField(max_length=250, blank=True, null=True)
    percent = models.CharField(max_length=250, blank=True, null=True, default=0)
