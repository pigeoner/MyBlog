# Generated by Django 3.2 on 2022-01-09 15:26

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211216_2130'),
        ('blog', '0010_auto_20220102_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='相册分类')),
                ('index', models.IntegerField(default=999, verbose_name='分类排序')),
            ],
            options={
                'verbose_name': '相册分类',
                'verbose_name_plural': '相册分类',
            },
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=blog.models.album_path, verbose_name='相册图片')),
                ('description', models.TextField(blank=True, default='图片', max_length=200, verbose_name='描述')),
                ('uploadTime', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.album', verbose_name='分类')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='上传用户')),
            ],
            options={
                'verbose_name': '相册数据',
                'verbose_name_plural': '相册数据',
            },
        ),
    ]
