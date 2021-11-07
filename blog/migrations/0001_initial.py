# Generated by Django 3.0.3 on 2021-11-07 16:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='标题')),
                ('author', models.CharField(default='', max_length=100, verbose_name='作者')),
                ('content', models.TextField(blank=True, default='', verbose_name='正文')),
                ('upload_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布日期')),
            ],
            options={
                'db_table': 'blogInfo',
            },
        ),
    ]
