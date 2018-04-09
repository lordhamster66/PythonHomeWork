#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/10/29
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def category_all(kwargs):
    """
    {% if kwargs.category_id == 0 %}
        <a class="active" href="/backend/article-0-{{ kwargs.article_type_id }}.html">全部</a>
    {% else %}
        <a href="/backend/article-0-{{ kwargs.article_type_id }}.html">全部</a>
    {% endif %}
    :return:
    """
    if kwargs["category_id"] == 0:  # 如过当前category_id等于0则激活分类的全部按钮
        ret = '<a class="active" href="/backend/article-0-%s.html">全部</a>' % kwargs["article_type_id"]
    else:
        ret = '<a href="/backend/article-0-%s.html">全部</a>' % kwargs["article_type_id"]
    return mark_safe(ret)


@register.simple_tag
def category_comment(category_list, kwargs):
    """
    {% for obj in category_list %}
        {% if obj.nid == kwargs.category_id %}
            <a class="active"
               href="/backend/article-{{ obj.nid }}-{{ kwargs.article_type_id }}.html">{{ obj.title }}</a>
        {% else %}
            <a href="/backend/article-{{ obj.nid }}-{{ kwargs.article_type_id }}.html">{{ obj.title }}</a>
        {% endif %}
    {% endfor %}
    :return:
    """
    temp_list = []  # 存放所有分类按钮标签
    for obj in category_list:
        if obj.nid == kwargs["category_id"]:  # 如果当前选择的分类id和此次循环的对象id相同则激活该按钮
            ret = '<a class="active" href="/backend/article-%s-%s.html">%s</a>' % (
                obj.nid,
                kwargs["article_type_id"],
                obj.title,
            )
            temp_list.append(ret)
        else:
            ret = '<a href="/backend/article-%s-%s.html">%s</a>' % (
                obj.nid,
                kwargs["article_type_id"],
                obj.title,
            )
            temp_list.append(ret)
    ret = "".join(temp_list)
    return mark_safe(ret)


@register.simple_tag
def article_type_all(kwargs):
    """
    {% if kwargs.article_type_id == 0 %}
        <a class="active" href="/backend/article-{{ kwargs.category_id }}-0.html">全部</a>
    {% else %}
        <a href="/backend/article-{{ kwargs.category_id }}-0.html">全部</a>
    {% endif %}
    :param kwargs:
    :return:
    """
    if kwargs["article_type_id"] == 0:
        ret = '<a class="active" href="/backend/article-%s-0.html">全部</a>' % kwargs["category_id"]
    else:
        ret = '<a href="/backend/article-%s-0.html">全部</a>' % kwargs["category_id"]
    return mark_safe(ret)


@register.simple_tag
def article_type_comment(article_type_list, kwargs):
    """
    {% for obj in article_type_list %}
        {% if obj.nid == kwargs.article_type_id %}
            <a class="active"
               href="/backend/article-{{ kwargs.category_id }}-{{ obj.nid }}.html">{{ obj.type }}</a>
        {% else %}
            <a href="/backend/article-{{ kwargs.category_id }}-{{ obj.nid }}.html">{{ obj.type }}</a>
        {% endif %}
    {% endfor %}
    :return:
    """
    temp_list = []
    for obj in article_type_list:
        if obj.nid == kwargs["article_type_id"]:
            temp_list.append(
                '<a class="active" href="/backend/article-%s-%s.html">%s</a>' % (
                    kwargs["category_id"],
                    obj.nid,
                    obj.type,
                )
            )
        else:
            temp_list.append(
                '<a href="/backend/article-%s-%s.html">%s</a>' % (
                    kwargs["category_id"],
                    obj.nid,
                    obj.type,
                )
            )
    return mark_safe("".join(temp_list))
