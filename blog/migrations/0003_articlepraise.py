# Generated by Django 3.2 on 2021-12-05 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_article_excerpt'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePraise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(verbose_name='点赞用户')),
                ('articleId', models.IntegerField(verbose_name='点赞文章')),
                ('praiseTime', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
            ],
            options={
                'verbose_name': '点赞数据',
                'verbose_name_plural': '点赞数据',
            },
        ),
    ]