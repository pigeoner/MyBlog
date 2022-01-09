from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, update_last_login
from users.models import UserProfile
from mdeditor.fields import MDTextField
from django.urls import reverse
import time
from django.utils.functional import cached_property  # 缓存装饰器
from django.template.loader import render_to_string  # 渲染模板
import markdown
from django.utils.html import strip_tags
from django.utils import timezone
import base64

# Create your models here.


# 文章分类
class Category(models.Model):
    name = models.CharField('博客分类', max_length=100)
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
    def category_base64(self):
        return base64.b64encode(self.name.encode('utf8')).decode('utf8')


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=100)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def tag_base64(self):
        return base64.b64encode(self.name.encode('utf8')).decode('utf8')


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(
        'cover/post_'+str(instance.user)+'_'+str(int(time.time())), ext)
    return filename  # 系统路径分隔符差异，增强代码重用性

# 文章


class Article(models.Model):
    title = models.CharField('标题', max_length=70, null=False, default='无标题')
    excerpt = models.TextField(
        '摘要', max_length=200, blank=True, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, verbose_name='分类', 
        null=False, default=5  # 默认为“其他”
    )
    # 使用外键关联分类表与分类是一对多关系
    tags = models.ManyToManyField(
        Tag, verbose_name='标签', 
        null=False, default=15  # 默认为“其他”
    )
    # 使用外键关联标签表与标签是多对多关系
    img = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='文章图片', 
        blank=True, null=False, default='cover/default.jpg'
    )
    # body = RichTextField('内容', width=800, height=500,
    #                      toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                      upload_settings={"imageMaxSize": 1204000},
    #                      settings={}, command=None, blank=True
    #                      )
    body = MDTextField(verbose_name='内容')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='作者')
    """
        文章作者，这里User是从django.contrib.auth.models导入的。
        这里我们通过 ForeignKey 把文章和 User 关联了起来。
        """
    views = models.PositiveIntegerField('阅读量', default=0, editable=False)
    thumbs_up = models.PositiveIntegerField('点赞数', default=0, editable=False)
    star = models.PositiveIntegerField('收藏数', default=0, editable=False)
    comments = models.PositiveBigIntegerField('评论数', default=0, editable=False)

    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def increase_thumbs_up(self):
        self.thumbs_up += 1
        self.save(update_fields=['thumbs_up'])

    def increase_comments(self):
        self.comments += 1
        self.save(update_fields=['comments'])

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:190]

        super().save(*args, **kwargs)


class ArticlePraise(models.Model):
    # userId = models.IntegerField('点赞用户')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='点赞用户')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='点赞文章')
    praiseTime = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞数据'
        verbose_name_plural = '点赞数据'

    def __str__(self) -> str:
        return 'Article '+str(self.article.id)+' praised by '+self.user.nick_name


class ArticleStar(models.Model):
    # userId = models.IntegerField('收藏用户')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='收藏用户')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='收藏文章')
    starTime = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏数据'
        verbose_name_plural = '收藏数据'

    def __str__(self) -> str:
        return 'Article '+str(self.article.id)+' stared by '+self.user.nick_name


class Follow(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='用户', related_name='fo_user')
    followUser = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='关注用户', related_name='follow_user')
    followTime = models.DateTimeField('关注时间', auto_now_add=True)

    class Meta:
        verbose_name = '关注数据'
        verbose_name_plural = '关注数据'

    def __str__(self) -> str:
        return '用户 '+self.user.nick_name+' 关注了 '+self.followUser.nick_name


class Fans(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='用户', related_name='fa_user')
    fans = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='粉丝', related_name='fans_user')
    fansTime = models.DateTimeField('粉丝关注时间', auto_now_add=True)

    class Meta:
        verbose_name = '粉丝数据'
        verbose_name_plural = '粉丝数据'

    def __str__(self) -> str:
        return '用户 '+self.user.nick_name+' 收获粉丝 '+self.fans.nick_name

# 侧边栏


class SideBar(models.Model):
    STATUS = (
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '热门文章'),
        (4, '文章归档'),
        (5, '标签云'),
        (6, '最近评论'),
        (7, 'HTML')
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(
        default=1, choices=DISPLAY_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, default='', verbose_name="内容",
                               help_text="如果设置的不是HTML类型，可为空")
    sort = models.PositiveIntegerField(
        default=1,  verbose_name="排序", help_text='序号越大越靠前')
    status = models.PositiveIntegerField(
        default=2, choices=STATUS, verbose_name="状态")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod    # 类方法装饰器，这个就变成了这个类的一个方法可以调用
    def get_sidebar(cls):
        return cls.objects.filter(status=2)   # 查询到所有允许展示的模块

    @property    # 成为一个类属性，调用的时候不需要后边的（）,是只读的，用户没办法修改
    def get_content(self):
        if self.display_type == 1:  # 搜索
            context = {}
            return render_to_string('../templates/blog/sidebar/search.html', context=context)
        elif self.display_type == 2:  # 最新文章
            context = {}
            return render_to_string('../templates/blog/sidebar/new_post.html', context=context)
        elif self.display_type == 3:  # 热门文章
            context = {}
            return render_to_string('../templates/blog/sidebar/hot_post.html', context=context)
        elif self.display_type == 4:   # 文章归档
            context = {}
            return render_to_string('../templates/blog/sidebar/archives.html', context=context)
        elif self.display_type == 5:   # 标签云
            context = {}
            return render_to_string('../templates/blog/sidebar/tags.html', context=context)
        elif self.display_type == 6:  # 最近评论
            context = {}
            return render_to_string('../templates/blog/sidebar/commment.html', context=context)
        elif self.display_type == 7:   # 自定义侧边栏

            return self.content   # 在侧边栏直接使用这里的html，模板中必须使用safe过滤器去渲染HTML


# 相册

def album_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(
        'album/album_'+str(instance.user)+'_'+str(int(time.time())), ext)
    return filename  # 系统路径分隔符差异，增强代码重用性

class Album(models.Model):
    name = models.CharField('相册分类', max_length=100)

    cover = models.ImageField(
        upload_to=album_path,
        verbose_name='相册封面',
        default='album/album_default.jpg'
    )

    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '相册分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

def album_pic_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(
        'album/pic_'+str(instance.user)+'_'+str(int(time.time())), ext)
    return filename  # 系统路径分隔符差异，增强代码重用性

class AlbumImage(models.Model):
    # userId = models.IntegerField('点赞用户')
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name='上传用户'
    )
    
    image = models.ImageField(
        upload_to=album_pic_path,
        verbose_name='相册图片'
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.DO_NOTHING,
        verbose_name='分类'
    )

    description = models.TextField('描述', max_length=200, blank=True, default='图片')

    uploadTime = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        verbose_name = '相册数据'
        verbose_name_plural = '相册数据'

    def __str__(self) -> str:
        return self.description