# Generated by Django 2.1.5 on 2019-02-12 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0004_auto_20190212_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadcontents',
            name='ddd',
        ),
        migrations.RemoveField(
            model_name='walletinformation',
            name='fromAccount',
        ),
        migrations.RemoveField(
            model_name='walletinformation',
            name='toAccount',
        ),
        migrations.AddField(
            model_name='uploadcontents',
            name='writername',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='walletinformation',
            name='posts_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unid.Post'),
        ),
    ]
