# Generated by Django 2.1.2 on 2019-02-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0021_auto_20190218_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundpost',
            name='expireDate',
            field=models.CharField(max_length=250, null=True),
        ),
    ]