# Generated by Django 2.1.2 on 2019-01-13 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unid', '0005_auto_20190113_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contentsinfo',
            old_name='uploadfilename',
            new_name='uploadzipfilename',
        ),
        migrations.AddField(
            model_name='contentsinfo',
            name='uploadfile',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uploadcontents',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]