from django.db import models

# Create your models here.

class TagInfo(models.Model):
    tagid = models.IntegerField('微信标签id', unique=True)
    tagname = models.CharField('微信标签名称', max_length=50)

    def __str__(self):
        return self.tagname

    class Meta:
        verbose_name = '企业微信标签'

class AgentInfo(models.Model):
    agentid = models.IntegerField('微信应用id', unique=True)
    name = models.CharField('微信应用名称', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '企业微信应用'

class TagUsersInfo(models.Model):
    tagid = models.CharField('微信标签id', max_length=10, unique=True)
    tagname = models.CharField('微信标签名称', max_length=50)
    userlist = models.TextField('标签成员列表', null=True)
    partylist = models.CharField('标签部门id列表', max_length=200, null=True)

    def __str__(self):
        return self.tagname

    class Meta:
        verbose_name = '企业微信标签成员'

class OrgInfo(models.Model):
    org_id = models.CharField('部门id', max_length=10, unique=True)
    name = models.CharField('部门名称', max_length=40)
    parent_id = models.CharField('父部门id', max_length=10)
    full_name = models.CharField('全称', max_length=200, null=True)
    tel = models.CharField('电话', max_length=20, null=True)
    property = models.CharField('部门属性', max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '组织信息表'


class EmployeInfo(models.Model):
    userid = models.CharField('成员id', max_length=30)
    name = models.CharField('成名名称', max_length=30)
    org_id = models.CharField('部门id', max_length=10)
    position = models.CharField('职位', max_length=30, null=True)
    leader = models.CharField('领导', max_length=4)
    mobile = models.CharField('手机号', max_length=20, null=True)
    email = models.CharField('邮箱', max_length=60, null=True)
    enable = models.CharField('是否启用', max_length=4)
    status = models.CharField('状态', max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '成员信息表'
