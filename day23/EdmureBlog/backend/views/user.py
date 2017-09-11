#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from repository import models
from backend.forms import BaseInfoForm


def login_decorate(func):
    def inner(request, *args, **kwargs):
        username = request.session.get("username", None)  # 获取session中的用户名
        if username:
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if user_obj:
                ret = func(request, *args, **kwargs)
            else:
                return redirect("/login.html")
        else:
            return redirect("/login.html")
        return ret

    return inner


@login_decorate
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if request.method == "GET":
        blog_obj = models.Blog.objects.filter(user__username=username).first()  # 获取用户博客信息
        if blog_obj:  # 能获取到则显示博客信息
            temp_dic = {
                "nickname": user_obj.nickname,
                "site": blog_obj.site,
                "theme": blog_obj.theme,
                "title": blog_obj.title,
            }
            base_info_obj = BaseInfoForm(temp_dic)  # 创建form对象，并设置默认值
        else:
            base_info_obj = BaseInfoForm()  # 没有博客信息则不设置默认值
        return render(request, 'backend_base_info.html', {"user_obj": user_obj, "base_info_obj": base_info_obj})
    elif request.method == "POST":
        base_info_obj = BaseInfoForm(request.POST)
        if base_info_obj.is_valid():
            site = base_info_obj.cleaned_data.get("site")
            title = base_info_obj.cleaned_data.get("title")
            theme = base_info_obj.cleaned_data.get("theme")
            nickname = base_info_obj.cleaned_data.get("nickname")
            blog_obj = models.Blog.objects.filter(user__username=username).first()  # 获取用户博客信息
            if blog_obj:  # 说明是更新操作
                if site == blog_obj.site:  # 如果使用的还是原来的站点
                    models.UserInfo.objects.filter(username=username).update(nickname=nickname)  # 更新用户信息
                    models.Blog.objects.filter(site=site).update(title=title, theme=theme)  # 更新博客信息
                else:  # 站点改变
                    obj = models.Blog.objects.filter(site=site).count()  # 使用站点查找博客对象
                    if obj:  # 能查到表明该站点已被使用
                        base_info_obj.add_error("site", "该站点已经存在！")
                        return render(request, 'backend_base_info.html',
                                      {"user_obj": user_obj, "base_info_obj": base_info_obj})
                    else:
                        models.UserInfo.objects.filter(username=username).update(nickname=nickname)  # 更新用户信息
                        # 更新博客信息
                        models.Blog.objects.filter(user__username=username).update(title=title, theme=theme, site=site)
            else:  # 说明是开通博客操作
                obj = models.Blog.objects.filter(site=site).count()  # 使用站点查找博客对象
                if obj:  # 能查到表明该站点已被使用
                    base_info_obj.add_error("site", "该站点已经存在！")
                    return render(request, 'backend_base_info.html',
                                  {"user_obj": user_obj, "base_info_obj": base_info_obj})
                else:  # 该站点没被使用，可以开通
                    models.UserInfo.objects.filter(username=username).update(nickname=nickname)  # 更新用户信息
                    # 创建博客
                    models.Blog.objects.create(
                        title=title,
                        site=site,
                        theme=theme,
                        user_id=user_obj.nid
                    )
            return redirect("/backend/base-info.html")
        else:
            return render(request, 'backend_base_info.html',
                          {"user_obj": user_obj, "base_info_obj": base_info_obj})


@login_decorate
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    return render(request, 'backend_tag.html')


def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    return render(request, 'backend_category.html')


def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    return render(request, 'backend_article.html')


def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    return render(request, 'backend_add_article.html')


def edit_article(request):
    """
    编辑文章
    :param request:
    :return:
    """
    return render(request, 'backend_edit_article.html')
