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


class District(models.Model):
    name = models.CharField('地名', max_length=255, default='')
    level = models.SmallIntegerField('等级')
    upid = models.IntegerField('隶属于', default=0)

    class Meta:
        db_table = 'district'
        ordering = ['id']

    # def __str__(self):
    #     _str = '地名：'+self.name+'\n等级：'+str(self.level)+'\n隶属于：'+str(self.upid)
    #     return _str
