#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from repository import models
from utils.pagination import Page


def index(request):
    """
    博客首页，展示全部博文
    :param request:  请求信息
    :param article_type: 文章类型
    :return:
    """
    if request.method == "GET":
        username = request.session.get("username", None)  # 获取session中的用户名
        user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
        article_type_list = models.ArticleType.objects.all()  # 获取所有的文章类型
        current_page = int(request.GET.get("p", "1"))  # 当前页码，默认是第一页
        article_type = request.GET.get("at", request.session.get("article_type"))  # 获取用户类型,获取不到则从session中获取
        request.session["article_type"] = article_type  # 将本次查询的文章类型存入session
        if article_type and article_type != "0":  # 有类型查询条件
            article_type = int(article_type)  # 先变成整数
            article_list = models.Article.objects.filter(
                article_type=article_type).all().select_related("blog", "blog__user")  # 依据类型获取所有的文章
        else:
            article_list = models.Article.objects.all().select_related("blog", "blog__user")  # 没有类型查询条件则获取所有文章
        data_count = len(article_list)  # 文章总个数
        page_obj = Page(current_page, data_count)  # 生成分页对象
        article_list = article_list[page_obj.start:page_obj.end]  # 获取当前页的所有文章
        page_str = page_obj.page_str("/")  # 获取分页html
        return render(request, 'index.html', {
            "article_type_list": article_type_list,  # 文章类型
            'article_list': article_list,  # 文章列表
            "page_str": page_str,  # 分页HTML
            "article_type": article_type,  # 文章类型ID
            "user_obj": user_obj,  # 用户对象
        })


def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi.html
    :return:
    """
    blog_obj = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog_obj:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog_obj)  # 获取博主所有的标签
    category_list = models.Category.objects.filter(blog=blog_obj)  # 获取博主所有的分类
    # date_format(create_time,"%Y-%m")
    date_list_sql = """select nid, count(nid) as num,strftime("%%Y-%%m",create_time) as ctime 
        from repository_article where blog_id = %s
        group by strftime("%%Y-%%m",create_time)
        """ % blog_obj.nid
    date_list = models.Article.objects.raw(date_list_sql)  # 获取博主文章所揽阔的月份
    article_list = models.Article.objects.filter(blog=blog_obj).order_by('-nid').all()
    current_page = int(request.GET.get("p", 1))  # 获取用户选择的页码，默认为第一页
    page_obj = Page(current_page, len(article_list))  # 获取分页对象
    page_str = page_obj.page_str("/%s.html" % site)  # 获取分页HTML
    article_list = article_list[page_obj.start:page_obj.end]  # 获取当前页数据
    return render(request, 'home.html', {
        'blog_obj': blog_obj,
        'tag_list': tag_list,
        'category_list': category_list,
        'date_list': date_list,
        'article_list': article_list,
        'page_str': page_str,
    })


def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog_obj = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog_obj:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog_obj)  # 获取博主所有的标签
    category_list = models.Category.objects.filter(blog=blog_obj)  # 获取博主所有的分类
    # date_format(create_time,"%Y-%m")
    date_list_sql = """select nid, count(nid) as num,strftime("%%Y-%%m",create_time) as ctime 
            from repository_article where blog_id = %s
            group by strftime("%%Y-%%m",create_time)
            """ % blog_obj.nid
    date_list = models.Article.objects.raw(date_list_sql)  # 获取博主文章所揽阔的月份
    template_name = "home_summary_list.html"
    if condition == 'tag':
        template_name = "home_title_list.html"
        article_list = models.Article.objects.filter(tags__title=val, blog=blog_obj).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category__title=val, blog=blog_obj).all()
    elif condition == 'date':
        article_list = models.Article.objects.filter(blog=blog_obj).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    else:
        article_list = []
    current_page = int(request.GET.get("p", 1))  # 获取用户选择的页码，默认为第一页
    page_obj = Page(current_page, len(article_list))  # 获取分页对象
    page_str = page_obj.page_str("/%s/%s/%s.html" % (site, condition, val))  # 获取分页HTML
    article_list = article_list[page_obj.start:page_obj.end]  # 获取当前页数据
    return render(request, template_name, {
        'blog_obj': blog_obj,
        'tag_list': tag_list,
        'category_list': category_list,
        'date_list': date_list,
        'article_list': article_list,
        'page_str': page_str,
    })


def detail(request, site, nid):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog_obj = models.Blog.objects.filter(site=site).select_related('user').first()
    return render(request, 'home_detail.html', {'blog_obj': blog_obj})
