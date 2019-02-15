# Generated by Django 2.1.3 on 2019-02-15 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0012_auto_20190215_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeusers',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AddField(
            model_name='post',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AddField(
            model_name='replyforposts',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unid.myPageInfomation'),
        ),
        migrations.AlterField(
            model_name='replyforposts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
