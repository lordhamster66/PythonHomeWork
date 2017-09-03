from django.contrib import admin
from report import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "pwd", "qq")

admin.site.register(models.User, UserAdmin)
