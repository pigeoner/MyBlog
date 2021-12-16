from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
    )

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='用户')
    nick_name = models.CharField('昵称', max_length=30, blank=True, default='')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField(
        '性别', max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField('地址', max_length=100, blank=True, default='')
    image = models.ImageField(
        upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=100, verbose_name='用户头像')
    sign = models.CharField('个性签名', max_length=30,
                            blank=True, default='这个人很懒，什么都没有写')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username
