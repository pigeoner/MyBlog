# Generated by Django 3.2 on 2022-01-02 13:19

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20211230_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(blank=True, default='cover/default.jpg', upload_to=blog.models.user_directory_path, verbose_name='文章图片'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='无标题', max_length=70, verbose_name='标题'),
        ),
    ]
