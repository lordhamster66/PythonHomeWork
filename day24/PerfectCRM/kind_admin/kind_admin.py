#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/11/11
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
from crm import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = ()  # 展示字段
    list_filter = ()  # 过滤字段
    search_fields = ()  # 检索字段
    list_per_page = 20  # 每页显示几条数据
    filter_horizontal = ()  # 显示复选框的字段
    ordering = None  # 默认排序字段
    default_actions = ("delete_selected",)  # 默认动作
    actions = ()  # 动作选项
    readonly_fields = ()  # 只读字段
    need_readonly = False  # 是否需要显示为只读
    table_readonly = False  # 整张表是否只读
    modelform_exclude_fields = ()  # model_form表单要剔除的字段
    dynamic_default_fields = ()  # 动态默认字段,在修改对象时动态生成
    only_display_img_field = ()  # 只显示图片的字段
    list_editable = ()  # 行内编辑字段
    field_color = {}  # 字段对应显示的颜色

    def delete_selected(self, request, querysets):
        """
        批量删除动作
        :param request: 请求内容
        :param querysets: 请求的所有对象
        :return:
        """
        app_name = self.model._meta.app_label  # APP名称
        table_name = self.model._meta.model_name  # 表名
        obj_ids = "-".join([str(i.id) for i in querysets])  # 拼接所有对象ID
        return redirect("/kind_admin/%s/%s/%s/delete/" % (app_name, table_name, obj_ids))

    delete_selected.display_name = "删除所选记录"


def register(model_class, admin_class=None):
    """注册表"""
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


class CustomerAdmin(BaseAdmin):
    list_display = (
        "id", "name", "qq", "source", "consult_course", "consultant", "status", "date",
        "add_customer_followup", "enroll"
    )
    list_filter = ("source", "consult_course", "consultant", "status", "date")
    search_fields = ("name", "qq")
    filter_horizontal = ("tags",)
    list_per_page = 10
    actions = ("aa",)
    modelform_exclude_fields = ("status",)
    readonly_fields = ("name", "qq", "qq_name", "phone", "person_id", "contact_email", "consultant", "status")
    field_color = {
        "status": {
            "0": ["red", "white"], "1": ["green", "white"], "2": ["yellow", "white"]
        }
    }

    # list_editable = ("status",)

    # table_readonly = True

    # ordering = "name"
    def aa(self, request, querysets):
        print("测试")
        return redirect("/crm/")

    aa.display_name = "测试"

    def add_customer_followup(self):
        return "<a href='/kind_admin/crm/customerfollowup/add/?" \
               "customer=%s&content=请填写跟进内容&consultant=%s&intention=2'>点击添加</a>" % (
                   self.instance.id, self.request.user.id
               )

    add_customer_followup.display_name = "添加跟进记录"

    def enroll(self):
        if self.instance.status == 0:
            info = "为其报名"
        else:
            info = "报名其他班级"
        return "<a href='/crm/sales/enrollment/%s/'>%s</a>" % (self.instance.id, info)

    enroll.display_name = "报名"

    def clean(self):
        pass

    def clean_name(self):
        pass


class TagAdmin(BaseAdmin):
    list_display = ("name", "date")


class CustomerFollowUPAdmin(BaseAdmin):
    list_display = ("customer", "consultant", "intention", "date")
    list_filter = ("customer", "consultant", "intention", "date")
    readonly_fields = ("customer", "consultant")


class CourseAdmin(BaseAdmin):
    list_display = ("name", "price", "period", "date")


class BranchAdmin(BaseAdmin):
    list_display = ("name",)


class ClassListAdmin(BaseAdmin):
    list_display = ("branch", "course", "class_type", "semester", "teachers", "start_date")


class ContractAdmin(BaseAdmin):
    list_display = ("name",)


class CourseRecordAdmin(BaseAdmin):
    list_display = ("from_class", "day_num", "teacher", "has_homework", "study_record")
    readonly_fields = ("from_class", "teacher")
    actions = ("create_study_record",)

    def create_study_record(self, request, querysets):
        """批量创建学习记录"""
        study_record_obj_list = []  # 存储学习记录对象
        for course_record_obj in querysets:
            for enrollment_obj in course_record_obj.from_class.enrollment_set.all():
                if enrollment_obj.contract_agreed and enrollment_obj.contract_approved:  # 学员同意合同且合同审核通过
                    study_record_obj_list.append(models.StudyRecord(
                        student=enrollment_obj,
                        course_record=course_record_obj,
                        attendance=0
                    ))
        try:
            models.StudyRecord.objects.bulk_create(study_record_obj_list)  # 批量生成学习记录
        except IntegrityError as e:  # 已经创建过该节上课记录的所有学习记录
            return render(request, "pages-403.html", {"errors": ["已经创建过该节上课记录的所有学习记录"]})
        return redirect(request.path)

    def study_record(self):
        """查看该节所有学习记录"""
        return "<a href='/kind_admin/crm/studyrecord/?course_record=%s'>点击查看</a>" % self.instance.id

    study_record.display_name = "该节所有学习记录"
    create_study_record.display_name = "创建所有学习记录"


class StudyRecordAdmin(BaseAdmin):
    """学习记录admin"""
    list_display = ("student", "course_record", "attendance", "check_homework", "score", "memo", "date")
    list_filter = ("student", "course_record", "attendance", "score", "date")
    list_editable = ("attendance", "score", "memo")
    readonly_fields = ("student", "course_record")
    field_color = {
        "attendance": {
            "0": ["green", "white"], "1": ["red", "white"], "2": ["yellow", "black"], "3": ["red", "white"]
        },
        "score": {
            "100": ["green", "white"], "90": ["#46b9d8", "white"], "85": ["#46b9d8", "white"],
            "80": ["#46b9d8", "white"], "75": ["blue", "white"], "70": ["blue", "white"],
            "60": ["blue", "white"], "40": ["yellow", "black"], "-50": ["yellow", "white"],
            "-100": ["red", "white"], "0": ["white", "black"]
        }
    }

    def check_homework(self):
        """查看可以下载的作业"""
        if self.instance.course_record.has_homework:
            return '''
            <button type="button" study-record-id="%s"
            class="btn btn-info check-homework" data-toggle="modal" 
            data-target=".bs-example-modal-sm">
            点击查看
            </button>''' % self.instance.id
        else:  # 没有作业
            return '没有作业'

    check_homework.display_name = "作业查看"


class EnrollmentAdmin(BaseAdmin):
    """报名表admin"""
    list_display = ("customer", "enrolled_class", "consultant", "contract_agreed", "contract_approved", "date")


class UserProfileAdmin(BaseAdmin):
    list_display = ("email", "name", "last_login", 'is_admin', "is_active")
    readonly_fields = ("email", "password",)
    filter_horizontal = ("roles", "groups", "user_permissions")
    modelform_exclude_fields = ("is_superuser", "last_login",)


class GroupAdmin(BaseAdmin):
    list_display = ("name",)
    filter_horizontal = ("permissions",)


class RoleAdmin(BaseAdmin):
    list_display = ("name",)
    filter_horizontal = ("menus",)


class MenuAdmin(BaseAdmin):
    list_display = ("name", "url_type", "url_name")


register(models.Customer, CustomerAdmin)
register(models.Tag, TagAdmin)
register(models.CustomerFollowUP, CustomerFollowUPAdmin)
register(models.Course, CourseAdmin)
register(models.Branch, BranchAdmin)
register(models.ClassList, ClassListAdmin)
register(models.Contract, ContractAdmin)
register(models.CourseRecord, CourseRecordAdmin)
register(models.StudyRecord, StudyRecordAdmin)
register(models.Enrollment, EnrollmentAdmin)
register(models.UserProfile, UserProfileAdmin)
register(Group, GroupAdmin)
register(models.Role, RoleAdmin)
register(models.Menu, MenuAdmin)
