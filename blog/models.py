from django.db import models
from datetime import datetime

# Create your models here.


class Blog(models.Model):
    title = models.CharField('标题', max_length=200, default='')
    author = models.CharField('作者', max_length=100, default='')
    content = models.TextField('正文', blank=True, default='')
    upload_time = models.DateTimeField('发布日期', default=datetime.now)

    class Meta:
        db_table = 'blogInfo'

    def __str__(self):
        _str = '标题：' + self.title + '\n作者：' + self.author + \
            '\n正文：' + self.content + '\n发布日期：' + str(self.upload_time)
        return _str
