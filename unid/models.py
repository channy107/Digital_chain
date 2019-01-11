from django.db import models
from django import forms
from datetime import datetime

class myPageInfomation(models.Model):
    # apiprovider = models.CharField(max_length=50, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(primary_key=True, max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    userimage = models.CharField(max_length=200, blank=True, null=True)
    profile = models.CharField(max_length=200, blank=True, null=True)
    joiningdate = models.DateTimeField(null=True)
    votingcount = models.IntegerField(blank=True, null=True)
    pwd = models.CharField(max_length=200, blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)


class wallet(models.Model):
    # IDX = models.AutoField(default=1)
    email = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    privateKey = models.CharField(max_length=100, blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    transactions = models.CharField(max_length=100, blank=True, null=True)



class uploadContents(models.Model):
    contents_id = models.AutoField(primary_key=True)
    writeremail = models.CharField(max_length=50)  # 기본키 설정??
    title = models.CharField(max_length=50)
    publisheddate = models.DateTimeField()
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    tags = models.CharField(max_length=50)
    fileinfo = models.CharField(max_length=250)
    totalpages = models.IntegerField()
    authorinfo = models.CharField(max_length=1000)
    intro = models.CharField(max_length=1000)
    index = models.CharField(max_length=1000)
    contents = models.CharField(max_length=1000)  # 소개글 제한?
    reference = models.CharField(max_length=1000, default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    downloadcount = models.IntegerField(null=True)
    isdelete = models.CharField(max_length=10, null=True)

class contentsInfo(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.IntegerField()
    uploadfilename = models.CharField(max_length=100)
    ftpsavefilename = models.CharField(max_length=100)
    contentspath = models.CharField(max_length=200)
    hash = models.CharField(max_length=150, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)

class previewInfo(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.IntegerField()
    uploadpreviewname = models.CharField(max_length=100)
    savepreviewname = models.CharField(max_length=100)
    imagepath = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    

class replysForContents(models.Model):
    IDX = models.AutoField(primary_key=True)
    contents_id = models.IntegerField()
    writeremail = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    replytext = models.CharField(max_length=1000, blank=True, null=True)




class Post(models.Model):
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='SOME STRING')
    contents = models.CharField(max_length=1000, default='SOME STRING')
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=False)
    category = models.CharField(max_length=50, default='SOME STRING')
    tags = models.CharField(max_length=100, default='SOME STRING')

class Like(models.Model):
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(myPageInfomation, on_delete=models.CASCADE)
    contents = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.contents

class walletInFormation(models.Model):
    transactiondate = models.DateTimeField(null=True)
    fromAccount = models.CharField(max_length=100, blank=True, null=True)
    toAccount = models.CharField(max_length=100, blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    txid = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)