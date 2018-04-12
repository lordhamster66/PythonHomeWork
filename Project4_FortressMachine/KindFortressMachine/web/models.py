from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class IDC(models.Model):
    """IDC"""
    name = models.CharField(max_length=64, unique=True, verbose_name="IDC名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "IDC表"


class Host(models.Model):
    """存储所有主机"""
    host_name = models.CharField(max_length=64, verbose_name="主机名称")
    ip_adr = models.GenericIPAddressField(unique=True, verbose_name="主机地址")
    port = models.PositiveSmallIntegerField(default=22, verbose_name="主机端口")
    idc = models.ForeignKey("IDC", verbose_name="对应IDC")

    enabled = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return self.ip_adr

    class Meta:
        verbose_name_plural = "主机表"


class HostGroup(models.Model):
    """主机组"""
    name = models.CharField(max_length=64, unique=True, verbose_name="主机组名称")
    bind_hosts = models.ManyToManyField("BindHost", blank=True, verbose_name="绑定的带账号的主机")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "主机组表"


class RemoteUser(models.Model):
    """远程账户"""
    username = models.CharField(max_length=64, verbose_name="远程账户名")
    auth_type_choices = ((0, "ssh/password"), (1, "ssh/key"))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0, verbose_name="登录类型")
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name="远程账户密码")

    def __str__(self):
        return "%s:%s(%s)" % (self.username, self.password, self.get_auth_type_display())

    class Meta:
        verbose_name_plural = "远程账户表"
        unique_together = ("username", "auth_type", "password")


class BindHost(models.Model):
    """绑定账号的主机"""
    host = models.ForeignKey("Host", verbose_name="绑定的主机")
    remote_user = models.ForeignKey("RemoteUser", verbose_name="绑定的远程用户")

    enabled = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return f"{self.remote_user.username}@{self.host.ip_adr}"

    class Meta:
        verbose_name_plural = "绑定账号的主机"
        unique_together = ("host", "remote_user")


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """堡垒机账户表"""
    email = models.EmailField(
        verbose_name='邮箱地址',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    bind_hosts = models.ManyToManyField("BindHost", blank=True, verbose_name="绑定的带账号的主机")
    host_groups = models.ManyToManyField("HostGroup", blank=True, verbose_name="绑定的主机组")

    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_admin = models.BooleanField(default=False, verbose_name="是否是管理员")
    is_staff = models.BooleanField(
        verbose_name="是否是员工",
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    class Meta:
        verbose_name_plural = "堡垒机账户表"


class Session(models.Model):
    """生成用户操作session id"""
    user = models.ForeignKey("UserProfile", verbose_name="用户")
    bind_host = models.ForeignKey("BindHost", verbose_name="操作的主机")
    tag = models.CharField(max_length=128, default="n/a", verbose_name="日志标识")
    closed = models.BooleanField(default=False, verbose_name="是否关闭")
    cmd_count = models.IntegerField(default=0, verbose_name="命令执行数量")  # 命令执行数量
    stay_time = models.IntegerField(default=0, help_text="每次刷新自动计算停留时间", verbose_name="停留时长(seconds)")
    date = models.DateTimeField(auto_now_add=True, verbose_name="查询时间")

    def __str__(self):
        return '<id:%s user:%s bind_host:%s>' % (self.id, self.user.email, self.bind_host.host)

    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'


class MultiTask(models.Model):
    """批量任务"""
    user = models.ForeignKey("UserProfile", verbose_name="批量任务执行者")
    task_type_choices = ((0, "cmd"), (1, "file_transfer"))
    task_type = models.SmallIntegerField(choices=task_type_choices, verbose_name="批量任务类型")
    content = models.TextField(verbose_name="批量任务内容")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="批量任务创建时间")

    def __str__(self):
        return f"{self.get_task_type_display()}-{self.content}"

    class Meta:
        verbose_name_plural = "批量任务记录"


class MultiTaskDetail(models.Model):
    """批量任务详细信息"""
    multi_task = models.ForeignKey("MultiTask", verbose_name="批量任务")
    bind_host = models.ForeignKey("BindHost", verbose_name="对应执行主机")
    result = models.TextField(verbose_name="执行结果")
    status_choices = ((0, "init"), (1, "success"), (2, "failed"))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="执行状态", default=0)

    start_time = models.DateTimeField(auto_now_add=True, verbose_name="执行任务创建时间")
    end_time = models.DateTimeField(verbose_name="执行任务终止时间", blank=True, null=True)

    def __str__(self):
        return f"{self.bind_host}-{self.status}"

    class Meta:
        unique_together = ("multi_task", "bind_host")
        verbose_name_plural = "批量任务详细信息"
