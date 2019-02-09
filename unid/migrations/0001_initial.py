# Generated by Django 2.1.2 on 2019-02-09 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='adBySuperUser',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('advertiser', models.CharField(max_length=100)),
                ('ad_path', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='blackReasonForBan',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('reason', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='contentsInfo',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('uploadzipfilename', models.CharField(max_length=100)),
                ('uploadfile', models.CharField(max_length=100, null=True)),
                ('contentspath', models.CharField(max_length=200)),
                ('hash', models.CharField(max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('filesize', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='downloadContents',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikeUsers',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('liked_users', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('rewards_success', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='myPageInfomation',
            fields=[
                ('IDX', models.IntegerField(null=True)),
                ('apiprovider', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('userimage', models.CharField(blank=True, max_length=200, null=True)),
                ('profile', models.CharField(blank=True, max_length=200, null=True)),
                ('joiningdate', models.DateTimeField(null=True)),
                ('votingcount', models.IntegerField(default=10)),
                ('pwd', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('like', models.IntegerField(null=True)),
                ('downloadedcontents', models.CharField(blank=True, max_length=250, null=True)),
                ('is_blacklist', models.CharField(blank=True, max_length=10, null=True)),
                ('blacklist_count', models.IntegerField(blank=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
                ('ddd', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='opinions',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('posts_id', models.IntegerField()),
                ('context', models.CharField(max_length=100)),
                ('fromuser', models.CharField(max_length=100)),
                ('writeruser', models.CharField(max_length=100)),
                ('exceptopinion', models.CharField(blank=True, max_length=250, null=True)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('type', models.CharField(blank=True, max_length=250, null=True)),
                ('result', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('posts_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=1000, null=True, upload_to='')),
                ('file_path', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=100)),
                ('contents', models.CharField(help_text='내용을 작성해주세요', max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.CharField(max_length=50)),
                ('tags', models.CharField(max_length=100)),
                ('rewards', models.FloatField(default=0)),
                ('rewards_success', models.CharField(blank=True, max_length=250, null=True)),
                ('like_count', models.IntegerField(default=0)),
                ('writer_rewards', models.CharField(blank=True, max_length=100, null=True)),
                ('category_path', models.CharField(blank=True, max_length=250, null=True)),
                ('isdelete', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='postImage',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('uploadfilename', models.CharField(max_length=100)),
                ('imagepath', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
                ('posts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.Post')),
            ],
        ),
        migrations.CreateModel(
            name='previewInfo',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('uploadpreviewname', models.CharField(max_length=100)),
                ('savepreviewname', models.CharField(max_length=100)),
                ('imagepath', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='replyForPosts',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('replytext', models.CharField(blank=True, max_length=1000, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
                ('posts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='replysForContents',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('replytext', models.CharField(blank=True, max_length=1000, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='superUser',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('log', models.CharField(max_length=50)),
                ('reason_for_modify', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='unidBlackList',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('is_blacklist', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('count', models.IntegerField()),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='uploadContents',
            fields=[
                ('contents_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('publisheddate', models.DateTimeField(null=True)),
                ('category', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('tags', models.CharField(max_length=50)),
                ('fileinfo', models.CharField(max_length=250)),
                ('authorinfo', models.CharField(max_length=1000)),
                ('intro', models.CharField(max_length=2000)),
                ('index', models.CharField(max_length=2000)),
                ('contents', models.CharField(max_length=2000)),
                ('reference', models.CharField(default=True, max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('downloadcount', models.IntegerField(null=True)),
                ('isdelete', models.CharField(max_length=10, null=True)),
                ('imagepath', models.CharField(max_length=200, null=True)),
                ('hits', models.IntegerField(default=0)),
                ('txid', models.CharField(blank=True, max_length=250, null=True)),
                ('replymentcount', models.IntegerField(null=True)),
                ('cagegory_path', models.CharField(blank=True, max_length=250, null=True)),
                ('ddd', models.CharField(blank=True, max_length=250, null=True)),
                ('writeremail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='walletInFormation',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('transactiondate', models.DateTimeField(editable=False, null=True)),
                ('fromAccount', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('toAccount', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('balance', models.FloatField(blank=True, editable=False, null=True)),
                ('txid', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('type', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('user', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('aaa', models.CharField(blank=True, max_length=250, null=True)),
                ('bbb', models.CharField(blank=True, max_length=250, null=True)),
                ('ccc', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='replysforcontents',
            name='contents_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.uploadContents'),
        ),
        migrations.AddField(
            model_name='replysforcontents',
            name='writeremail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AddField(
            model_name='previewinfo',
            name='contents_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.uploadContents'),
        ),
        migrations.AddField(
            model_name='likeusers',
            name='posts_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.Post'),
        ),
        migrations.AddField(
            model_name='downloadcontents',
            name='contents_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.uploadContents'),
        ),
        migrations.AddField(
            model_name='downloadcontents',
            name='downloader_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AddField(
            model_name='contentsinfo',
            name='contents_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.uploadContents'),
        ),
        migrations.AddField(
            model_name='blackreasonforban',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
    ]
