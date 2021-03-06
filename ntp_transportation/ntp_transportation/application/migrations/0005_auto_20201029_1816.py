# Generated by Django 2.2.16 on 2020-10-29 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20201027_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='receiverName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='receiverSurname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='senderName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='senderSurname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(default=123),
        ),
    ]
