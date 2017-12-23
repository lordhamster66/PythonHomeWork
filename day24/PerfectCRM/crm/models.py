from django.db import models

from django.contrib.auth.models import User  # django自带的账户认证表
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


# Create your models here.
class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="客户姓名")
    qq = models.CharField(max_length=64, unique=True, verbose_name="客户QQ")  # 不可以为空
    qq_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="qq名称")
    phone = models.CharField(max_length=64, blank=True, null=True, verbose_name="手机号")
    person_id = models.CharField(max_length=64, blank=True, null=True, verbose_name="身份证号")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="联系邮箱")
    source_choices = (
        (0, '转介绍'),
        (1, 'QQ'),
        (2, '官网'),
        (3, '百度推广'),
        (4, '51CTO'),
        (5, '知乎'),
        (6, '市场推广'),
    )
    source = models.SmallIntegerField(choices=source_choices, verbose_name="客户来源")
    referral_from = models.CharField(max_length=64, blank=True, null=True, verbose_name="转介绍人QQ")
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程")
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="标签")
    consultant = models.ForeignKey("UserProfile", verbose_name="顾问")
    memo = models.TextField(blank=True, null=True, verbose_name="备注")
    status_choices = (
        (0, "未报名"),
        (1, "已报名"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="报名状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = "客户信息表"


class Tag(models.Model):
    """标签表"""
    name = models.CharField(max_length=32, unique=True, verbose_name="标签名称")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "标签表"


class CustomerFollowUP(models.Model):
    """客户跟进记录表"""
    customer = models.ForeignKey("Customer", verbose_name="跟进客户")
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进顾问")
    intention_choices = (
        (0, "2周内报名"),
        (1, "1个月内报名"),
        (2, "近期无报名计划"),
        (3, "已在其它机构报名"),
        (4, "已报名"),
        (5, "已拉黑"),
    )
    intention = models.SmallIntegerField(choices=intention_choices, verbose_name="客户意向")
    date = models.DateTimeField(auto_now_add=True, verbose_name="跟进时间")

    def __str__(self):
        return "<%s %s>" % (self.customer.qq, self.intention)

    class Meta:
        verbose_name_plural = "客户跟进记录表"


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="课程名称")
    price = models.PositiveSmallIntegerField(verbose_name="课程价格")
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField(verbose_name="课程大纲")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "课程表"


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=128, unique=True, verbose_name="校区名称")
    addr = models.CharField(max_length=128, verbose_name="校区地址")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "校区表"


class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey("Branch", verbose_name="校区")
    course = models.ForeignKey("Course", verbose_name="课程")
    class_type_choices = (
        (0, "面授(脱产)"),
        (1, "面授(周末)"),
        (2, "网络班"),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile", verbose_name="老师")
    contract = models.ForeignKey("Contract", blank=True, null=True)
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(blank=True, null=True, verbose_name="结业日期")

    def __str__(self):
        return "<%s %s %s>" % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ("branch", "course", "semester")  # 校区课程和第几期需要联合唯一
        verbose_name_plural = "班级表"


class Contract(models.Model):
    """合同表"""
    name = models.CharField(max_length=64, verbose_name="合同名称")
    content = models.TextField(verbose_name="合同内容")

    def __str__(self):
        return "<%s>" % self.name

    class Meta:
        verbose_name_plural = "合同表"


class CourseRecord(models.Model):
    """上课记录表"""
    from_class = models.ForeignKey("ClassList", verbose_name="班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    teacher = models.ForeignKey("UserProfile", verbose_name="老师")
    has_homework = models.BooleanField(default=True, verbose_name="是否有作业")
    homework_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="作业标题")
    homework_content = models.TextField(blank=True, null=True, verbose_name="作业内容")
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True, verbose_name="创建日期")

    def __str__(self):
        return "<%s %s>" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name_plural = "上课记录表"


class StudyRecord(models.Model):
    """学习记录表"""
    student = models.ForeignKey("Enrollment", verbose_name="学生")
    course_record = models.ForeignKey("CourseRecord", verbose_name="上课记录")
    attendance_choices = (
        (0, "已签到"),
        (1, "迟到"),
        (2, "缺勤"),
        (3, "早退"),
    )
    attendance = models.SmallIntegerField(choices=attendance_choices, verbose_name="状态")
    score_choices = (
        (100, "A+"),
        (90, "A"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (-100, "COPY"),
        (0, "N/A"),
    )
    score = models.SmallIntegerField(choices=score_choices, default=0, verbose_name="成绩")
    memo = models.TextField(blank=True, null=True, verbose_name="备注")
    date = models.DateField(auto_now_add=True, verbose_name="创建日期")

    def __str__(self):
        return "<%s %s %s>" % (self.student, self.course_record, self.score)

    class Meta:
        unique_together = ("student", "course_record")
        verbose_name_plural = "学习记录表"


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer", verbose_name="学员")
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True, verbose_name="报名时间")

    def __str__(self):
        return "<%s %s>" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name_plural = "报名表"


class Payment(models.Model):
    """缴费记录"""
    customer = models.ForeignKey("Customer", verbose_name="客户")
    course = models.ForeignKey("Course", verbose_name="所报课程")
    amount = models.PositiveIntegerField(default=500, verbose_name="缴费数额")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    date = models.DateTimeField(auto_now_add=True, verbose_name="缴费时间")

    def __str__(self):
        return "<%s %s>" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = "缴费记录表"


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True, verbose_name="角色名称")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"


class Menu(models.Model):
    """动态菜单表"""
    name = models.CharField(unique=True, max_length=32, verbose_name="菜单名")
    url_type = models.SmallIntegerField(choices=((0, 'relative_name'), (1, 'absolute_url')), verbose_name="菜单url类型")
    url_name = models.CharField(unique=True, max_length=128, verbose_name="菜单url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "动态菜单表"


# class UserProfile(models.Model):
#     """账户表"""
#     user = models.OneToOneField(User, verbose_name="Django账户表")
#     name = models.CharField(max_length=32, verbose_name="姓名")
#     roles = models.ManyToManyField("Role", blank=True, verbose_name="所属角色")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "账户表"

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
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(
        _('password'),
        max_length=128,
        help_text=mark_safe("<a href='password/'>点我修改密码</a>")
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    roles = models.ManyToManyField("Role", blank=True, verbose_name="所属角色", default=None)

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

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_active

    class Meta:
        verbose_name_plural = "账户表"
        permissions = (
            ("can_access_sales_index", "可以访问销售首页"),
            ("can_access_table_index", "可以访问kind_admin下的APP库"),
            ("can_access_table_objs", "可以访问kind_admin下注册的所有表"),
            ("can_do_action_or_change_table_objs", "可以对kind_admin下注册的所有表进行行内编辑和action操作"),
            ("can_access_table_change", "可以访问kind_admin下注册的所有表的对象修改页"),
            ("can_change_table_obj", "可以修改kind_admin下注册的所有表的对象"),
            ("can_access_table_delete", "可以访问kind_admin下注册的所有表的删除页"),
            ("can_delete_all_table_obj", "可以删除kind_admin下注册的所有表的信息"),
            ("can_access_table_add", "可以访问kind_admin下注册的所有表的增加信息页"),
            ("can_add_all_table_obj", "可以增加kind_admin下注册的所有表的信息"),
            ("can_access_customer_table", "可以访问kind_admin下注册的客户库"),
            ("can_access_customer_add", "可以访问在kind_admin下注册的客户库添加客户页面"),
            ("can_add_customer", "可以在kind_admin下注册的客户库添加客户"),
            ("can_access_customer_change", "可以访问在kind_admin下注册的客户库所生成的客户修改页"),
            ("can_change_customer", "可以修改在kind_admin下注册的客户库中的客户,且只能修改自己的客户"),
            ("can_access_change_password", "可以访问密码修改页"),
            ("can_change_own_password", "可以修改自己的密码"),
            ("can_change_all_password", "可以修改所有人的密码"),
        )
