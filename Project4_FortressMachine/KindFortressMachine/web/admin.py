from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from web import models


# Register your models here.
class IDCAdmin(admin.ModelAdmin):
    list_display = ("name",)


class HostAdmin(admin.ModelAdmin):
    list_display = ("host_name", "ip_adr", "port", "idc", "enabled")


class HostGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("bind_hosts",)


class RemoteUserAdmin(admin.ModelAdmin):
    list_display = ("username", "auth_type", "password")


class BindHostAdmin(admin.ModelAdmin):
    list_display = ("host", "remote_user")


class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "bind_host", "date")


class MultiTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "task_type", "createtime")


class MultiTaskDetailAdmin(admin.ModelAdmin):
    list_display = ("multi_task_id", "multi_task", "bind_host", "status", "result", "start_time", "end_time")


admin.site.register(models.IDC, IDCAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.RemoteUser, RemoteUserAdmin)
admin.site.register(models.BindHost, BindHostAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.MultiTask, MultiTaskAdmin)
admin.site.register(models.MultiTaskDetail, MultiTaskDetailAdmin)


# 账户表的Admin配置
class UserProfileCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_active', 'is_admin', 'is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('个人信息', {'fields': ('name',)}),
        ('主机管理', {'fields': ('bind_hosts', "host_groups")}),
        ('权限管理', {'fields': ('is_active', 'is_admin', 'is_staff', 'groups', "user_permissions")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', "user_permissions", 'bind_hosts', "host_groups")
    # list_editable = ("is_active",)


# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
