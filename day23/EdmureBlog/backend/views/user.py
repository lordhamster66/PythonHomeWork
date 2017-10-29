#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from repository import models
from backend.forms import BaseInfoForm
from backend.forms import TagForm
from backend.forms import CategoryForm
from utils.public import create_id
from EdmureBlog import settings
from utils.pagination import Page


def login_decorate(func):
    """登录验证装饰器"""

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
def index(request):
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).first()
    return render(request, 'backend_index.html', {"user_obj": user_obj})


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
                          {"user_obj": user_obj, "base_info_obj": base_info_obj}
                          )


@login_decorate
def tag(request):
    """

    博主个人标签管理
    :param request:
    :return:
    """
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
    tag_list = models.Tag.objects.filter(blog_id=user_obj.blog.nid).all()  # 获取用户所有标签
    if request.method == "GET":
        current_page = int(request.GET.get("p", 1))  # 获取用户选择的页码，默认为第一页
        page_obj = Page(current_page, len(tag_list))  # 获取分页对象
        page_str = page_obj.page_str("/backend/tag.html")  # 获取分页HTML
        tag_list = tag_list[page_obj.start:page_obj.end]  # 获取当前页数据
        tag_obj = TagForm()  # 生成标签form对象
        return render(request, 'backend_tag.html', {
            "user_obj": user_obj, "tag_list": tag_list, "tag_obj": tag_obj, "page_str": page_str
        })
    elif request.method == "POST":
        tag_obj = TagForm(request.POST)
        if tag_obj.is_valid():  # tagform验证通过
            tagname = tag_obj.cleaned_data.get("tagname")  # 获取新加的tagname
            if models.Tag.objects.filter(blog_id=user_obj.blog.nid, title=tagname).count():  # 检测tagname是否存在
                tag_obj.add_error("tagname", "该标签名已经存在！")
            else:  # 不存在则创建
                models.Tag.objects.create(
                    title=tagname,
                    blog_id=user_obj.blog.nid
                )
        page_obj = Page(1, len(tag_list))  # 获取分页对象
        page_str = page_obj.page_str("/backend/tag.html")  # 获取分页HTML
        tag_list = tag_list[page_obj.start:page_obj.end]  # 获取当前页数据
        return render(request, 'backend_tag.html', {
            "user_obj": user_obj, "tag_list": tag_list, "tag_obj": tag_obj, "page_str": page_str
        })


def delete_tag(request):
    """删除标签功能"""
    if request.method == "POST":
        tag_nid = request.POST.get("nid")  # 获取用户想要删除的标签ID
        models.Tag.objects.filter(nid=tag_nid).delete()  # 删除用户选择的标签
        ret = {"status": True, "data": None}
        return HttpResponse(json.dumps(ret))


def update_tag(request):
    """保存标签功能"""
    ret = {"status": True, "errors": None, "data": None}
    if request.method == "POST":
        tag_nid = request.POST.get("nid")  # 获取用户想要更新的标签ID
        tag_name = request.POST.get("info_name")  # 获取用户想要更新的标签名称
        tag_obj = models.Tag.objects.filter(nid=tag_nid).first()
        if tag_name == tag_obj.title:
            ret["status"] = False
            ret["errors"] = "输入的标签名称和原有一样！不需要更新!"
        else:
            tag_obj_by_tag_name = models.Tag.objects.filter(title=tag_name).first()
            if tag_obj_by_tag_name:
                ret["status"] = False
                ret["errors"] = "输入的标签名称已存在，请重新输入！"
            else:
                tag_obj.title = tag_name  # 更新标签名称
                tag_obj.save()  # 保存更新好的标签对象
    return HttpResponse(json.dumps(ret))


@login_decorate
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
    category_list = models.Category.objects.filter(blog_id=user_obj.blog.nid).all()  # 获取用户的文章分类
    if request.method == "GET":
        current_page = int(request.GET.get("p", 1))  # 获取用户选择的页码，默认为第一页
        page_obj = Page(current_page, len(category_list))  # 获取分页对象
        page_str = page_obj.page_str("/backend/category.html")  # 获取分页HTML
        category_list = category_list[page_obj.start:page_obj.end]  # 获取当前页数据
        category_obj = CategoryForm()
        return render(request, 'backend_category.html',
                      {"user_obj": user_obj,
                       "category_list": category_list,
                       "category_obj": category_obj,
                       "page_str": page_str,
                       })
    elif request.method == "POST":
        category_obj = CategoryForm(request.POST)
        if category_obj.is_valid():  # categoryform验证通过
            category = category_obj.cleaned_data.get("category")  # category
            if models.Category.objects.filter(blog_id=user_obj.blog.nid, title=category).count():  # 检测category是否存在
                category_obj.add_error("category", "该分类名称已经存在！")
            else:  # 不存在则创建
                models.Category.objects.create(
                    title=category,
                    blog_id=user_obj.blog.nid
                )
        page_obj = Page(1, len(category_list))  # 获取分页对象
        page_str = page_obj.page_str("/backend/category.html")  # 获取分页HTML
        category_list = category_list[page_obj.start:page_obj.end]  # 获取当前页数据
        return render(request, 'backend_category.html',
                      {"user_obj": user_obj,
                       "category_list": category_list,
                       "category_obj": category_obj,
                       "page_str": page_str, })


def delete_category(request):
    """删除分类功能"""
    if request.method == "POST":
        category_nid = request.POST.get("nid")  # 获取用户想要删除的分类ID
        models.Category.objects.filter(nid=category_nid).delete()  # 删除用户选择的分类
        ret = {"status": True, "data": None}
        return HttpResponse(json.dumps(ret))


def update_category(request):
    """更新分类功能"""
    ret = {"status": True, "errors": None, "data": None}
    if request.method == "POST":
        category_nid = request.POST.get("nid")  # 获取用户想要更新的分类ID
        category_name = request.POST.get("info_name")  # 获取用户想要更新的分类名称
        category_obj = models.Category.objects.filter(nid=category_nid).first()
        if category_name == category_obj.title:
            ret["status"] = False
            ret["errors"] = "输入的分类名称和原有一样！不需要更新!"
        else:
            category_obj_by_category_name = models.Category.objects.filter(title=category_name).first()
            if category_obj_by_category_name:
                ret["status"] = False
                ret["errors"] = "输入的分类名称已存在，请重新输入！"
            else:
                category_obj.title = category_name  # 更新分类名称
                category_obj.save()  # 保存更新好的分类对象
    return HttpResponse(json.dumps(ret))


@login_decorate
def article(request, *args, **kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    condition = {}  # 筛选条件
    for k, v in kwargs.items():
        kwargs[k] = int(v)  # 将字符串改为数字
        if v != "0":
            condition[k] = v
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
    category_list = models.Category.objects.filter(blog_id=user_obj.blog.nid).all()  # 获取用户博客的所有分类
    article_type_list = models.ArticleType.objects.all()  # 获取文章类型
    article_list = models.Article.objects.filter(blog_id=user_obj.blog.nid).filter(**condition).all()  # 获取用户的文章
    if request.method == "GET":
        current_page = int(request.GET.get("p", 1))  # 获取用户选择的页码，默认为第一页
        page_obj = Page(current_page, len(article_list))  # 获取分页对象
        page_str = page_obj.page_str("/backend/article.html")  # 获取分页HTML
        article_list = article_list[page_obj.start:page_obj.end]  # 获取当前页数据
        return render(
            request, 'backend_article.html', {
                "user_obj": user_obj,  # 用户对象
                "category_list": category_list,  # 博客分类列表
                "article_type_list": article_type_list,  # 文章分类
                "article_list": article_list,  # 文章列表
                "page_str": page_str,  # 分页对象
                "kwargs": kwargs,  # 用户文章分类和博客分类
            }
        )


def delete_article(request):
    """删除文章"""
    if request.method == "POST":
        article_nid = request.POST.get("nid")  # 获取用户想要删除的文章ID
        models.Article.objects.filter(nid=article_nid).delete()  # 删除用户选择的文章
        ret = {"status": True, "data": None}
        return HttpResponse(json.dumps(ret))


def update_article(request):
    """更新文章标题"""
    ret = {"status": True, "errors": None, "data": None}
    if request.method == "POST":
        article_nid = request.POST.get("nid")  # 获取用户想要更新的文章ID
        article_name = request.POST.get("info_name")  # 获取用户想要更新的文章标题
        article_obj = models.Article.objects.filter(nid=article_nid).first()
        if article_name == article_obj.title:
            ret["status"] = False
            ret["errors"] = "输入的文章标题和原有一样！不需要更新!"
        else:
            article_obj_by_article_name = models.Article.objects.filter(title=article_name).first()
            if article_obj_by_article_name:
                ret["status"] = False
                ret["errors"] = "输入的文章标题已存在，请重新输入！"
            else:
                models.Article.objects.filter(nid=article_nid).update(title=article_name)
    return HttpResponse(json.dumps(ret))


def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
    return render(request, 'backend_add_article.html', {"user_obj": user_obj})


def edit_article(request, nid):
    """
    编辑文章
    :param request:
    :return:
    """
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
    return render(request, 'backend_edit_article.html', {"user_obj": user_obj})


def upload_head_portrait(request):
    """上传头像功能"""
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).first()  # 获取用户名对应的用户对象
    avatar = request.FILES.get("head_portrait")  # 获取用户上传的文件
    file_name = create_id()  # 生成随机文件名
    file_path = os.path.join(settings.BASE_DIR, "static", "imgs", "avatar", "%s.png" % file_name)  # 获取文件路径
    # 写入服务器
    with open(file_path, "wb") as f:
        for line in avatar:
            f.write(line)
    user_obj.avatar = file_name  # 用户头像为头像文件名
    user_obj.save()  # 存储用户对象
    ret = {"status": True, "data": None}
    return HttpResponse(json.dumps(ret))


def revoke_head_portrait(request):
    """撤销头像功能"""
    username = request.session.get("username", None)  # 获取session中的用户名
    user_obj = models.UserInfo.objects.filter(username=username).first()  # 获取用户名对应的用户对象
    user_obj.avatar = "default"  # 将用户头像置为默认
    user_obj.save()  # 存储用户对象
    ret = {"status": True, "data": None}
    return HttpResponse(json.dumps(ret))
