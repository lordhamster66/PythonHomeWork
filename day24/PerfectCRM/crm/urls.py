"""PerfectCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^$', views.index),  # crm首页
    url(r'^sales/$', views.sales_index, name="sales_index"),  # 销售首页
    url(r'^sales/enrollment/(?P<customer_id>\d+)/$', views.enrollment, name="enrollment_for_customer"),  # 给客户报名
    url(r'^customer/registration/(?P<enrollment_id>\d+)/(?P<random_str>\w+)/$',
        views.customer_registration, name="customer_registration"),  # 客户填写报名信息
    url(r'^upload_identity_photo/$', views.upload_identity_photo, name="upload_identity_photo"),  # 上传身份证照片
]
