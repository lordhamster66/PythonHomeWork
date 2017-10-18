from django.conf.urls import url
from django.conf.urls import include
from .views import user

urlpatterns = [
    url(r'^base-info.html$', user.base_info),  # 用户基本信息
    url(r'^tag.html$', user.tag),  # 标签管理页面
    url(r'^category.html$', user.category),  # 分类管理页面
    url(r'^article.html$', user.article),  # 文章管理页面
    url(r'^add-article.html$', user.add_article),  # 添加文章
    url(r'^edit-article-(\d+).html$', user.edit_article),  # 编辑文章
    url(r'^upload_head_portrait/$', user.upload_head_portrait),  # 上传头像
    url(r'^revoke_head_portrait/$', user.revoke_head_portrait),  # 撤销头像
    url(r'^delete_tag/$', user.delete_tag),  # 删除标签
    url(r'^update_tag/$', user.update_tag),  # 更新标签
]
