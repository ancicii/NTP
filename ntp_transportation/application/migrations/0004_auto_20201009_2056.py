# Generated by Django 2.2.16 on 2020-10-09 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20201009_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
