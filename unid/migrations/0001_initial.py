# Generated by Django 2.1.2 on 2019-01-08 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='contentsInfo',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('contents_id', models.IntegerField()),
                ('uploadfilename', models.CharField(max_length=100)),
                ('ftpsavefilename', models.CharField(max_length=100)),
                ('contentspath', models.CharField(max_length=200)),
                ('hash', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='myPageInfomation',
            fields=[
                ('apiprovider', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('userimage', models.CharField(blank=True, max_length=200, null=True)),
                ('profile', models.CharField(blank=True, max_length=200, null=True)),
                ('joiningdate', models.DateTimeField(null=True)),
                ('votingcount', models.IntegerField(blank=True, null=True)),
                ('pwd', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, null=True, upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('contents', models.CharField(help_text='내용을 작성해주세요', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=50)),
                ('tags', models.CharField(max_length=100, null=True)),
                ('like_user_set', models.ManyToManyField(blank=True, related_name='like_user_set', through='unid.Like', to='unid.myPageInfomation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='previewInfo',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('contents_id', models.IntegerField()),
                ('uploadpreviewname', models.CharField(max_length=100)),
                ('ftpsavepreviewname', models.CharField(max_length=100)),
                ('imagepath', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='replysForContents',
            fields=[
                ('IDX', models.AutoField(primary_key=True, serialize=False)),
                ('contents_id', models.IntegerField()),
                ('writeremail', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('replytext', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='uploadContents',
            fields=[
                ('contents_id', models.AutoField(primary_key=True, serialize=False)),
                ('writeremail', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('publisheddate', models.DateTimeField()),
                ('category', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('tags', models.CharField(max_length=50)),
                ('fileinfo', models.CharField(max_length=250)),
                ('totalpages', models.IntegerField()),
                ('previewpath', models.CharField(max_length=250)),
                ('authorinfo', models.CharField(max_length=1000)),
                ('intro', models.CharField(max_length=1000)),
                ('index', models.CharField(max_length=1000)),
                ('contents', models.CharField(max_length=1000)),
                ('reference', models.CharField(default=True, max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.CharField(blank=True, max_length=100, null=True)),
                ('privateKey', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.IntegerField(blank=True, null=True)),
                ('transactions', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='walletInFormation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactiondate', models.DateTimeField(null=True)),
                ('fromAccount', models.CharField(blank=True, max_length=100, null=True)),
                ('toAccount', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.IntegerField(blank=True, null=True)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'post')},
        ),
    ]