# Generated by Django 2.2.16 on 2020-10-24 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destinations', models.TextField(null=True)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train', to='application.Train')),
            ],
        ),
    ]
