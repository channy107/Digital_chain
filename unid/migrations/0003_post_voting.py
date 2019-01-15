# Generated by Django 2.1.2 on 2019-01-12 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0002_auto_20190111_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('posts_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=1000, null=True, upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('contents', models.CharField(help_text='내용을 작성해주세요', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.CharField(max_length=50)),
                ('tags', models.CharField(max_length=100)),
                ('rewards', models.FloatField(default=0)),
                ('liked_users', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation')),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('votings_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('posts_id', models.CharField(max_length=1000)),
                ('voting_count', models.IntegerField(default=0)),
            ],
        ),
    ]