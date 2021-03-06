# Generated by Django 3.2 on 2021-12-30 06:57

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20211220_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(blank=True, default='cover/Django.jpg', upload_to=blog.models.user_directory_path, verbose_name='文章图片'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(default=15, to='blog.Tag', verbose_name='标签'),
        ),
    ]
