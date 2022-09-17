from django.db import models

# Create your models here.

class DBSource(models.Model):
    name = models.CharField('名称', max_length=50, unique=True)
    address = models.CharField('数据库地址', max_length=60)
    port = models.IntegerField('数据库端口', default=3306)
    database = models.CharField('数据库名', max_length=30)
    user = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '数据源'

class Tag(models.Model):
    name = models.CharField('标签名称', max_length=50, unique=True)
    sql = models.TextField('sql语句')
    group = models.ForeignKey('TagGroup', on_delete=models.PROTECT, blank=True, related_name='group_tag')
    dbsource = models.ForeignKey('DBSource', on_delete=models.PROTECT, blank=True, related_name='dbsource_tag')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '数据标签'

class TagGroup(models.Model):
    name = models.CharField('标签组名称', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '数据标签组'
        ordering = ['id']

class EmailGroup(models.Model):
    name = models.CharField('邮箱组名称', max_length=20, unique=True)
    email_list = models.TextField('邮箱列表')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '邮箱组'