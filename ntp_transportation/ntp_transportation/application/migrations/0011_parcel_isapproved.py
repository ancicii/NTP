# Generated by Django 2.2.16 on 2020-10-31 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20201030_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='isApproved',
            field=models.BooleanField(default=True),
        ),
    ]
