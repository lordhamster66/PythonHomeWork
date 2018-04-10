from django.conf.urls import url
from web.views import account
from web.views import home
from web.views import asset
from web.views import server
from web.views import user
from web.views import business_unit
from web.views import idc
from web.views import tag
from web.views import error_log

urlpatterns = [
    url(r'^login.html$', account.LoginView.as_view()),  # 登录
    url(r'^logout.html$', account.LogoutView.as_view()),  # 注销
    url(r'^index.html$', home.IndexView.as_view()),  # 平台首页
    # 以下均为资产相关
    url(r'^cmdb.html$', home.CmdbView.as_view(), name="cmdb_index"),  # 资产首页
    url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),  # 获取图表数据

    # 资产管理
    url(r'^asset.html$', asset.AssetListView.as_view(), name="asset_index"),
    url(r'^assets.html$', asset.AssetJsonView.as_view(), name="asset_json"),

    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view(), name="add_asset"),

    # 服务器管理
    url(r'^servers.html$', server.ServerJsonView.as_view(), name="server_json"),
    url(r'^add-server.html$', server.AddServerView.as_view(), name="add_server"),

    # 用户管理
    url(r'^user.html$', user.UserListView.as_view(), name="user_index"),
    url(r'^users.html$', user.UserJsonView.as_view(), name="user_json"),
    url(r'^add-user.html$', user.AddUserView.as_view(), name="add_user"),

    # 业务管理
    url(r'^business_unit.html$', business_unit.BusinessUnitListView.as_view(), name="business_unit_index"),
    url(r'^business_units.html$', business_unit.BusinessUnitJsonView.as_view(), name="business_unit_json"),
    url(r'^add-business_unit.html$', business_unit.AddBusinessUnitView.as_view(), name="add_business_unit"),

    # IDC管理
    url(r'^idc.html$', idc.IDCListView.as_view(), name="idc_index"),
    url(r'^idcs.html$', idc.IDCJsonView.as_view(), name="idc_json"),
    url(r'^add-idc.html$', idc.AddIDCView.as_view(), name="add_idc"),

    # 标签管理
    url(r'^tag.html$', tag.TagListView.as_view(), name="tag_index"),
    url(r'^tags.html$', tag.TagJsonView.as_view(), name="tag_json"),
    url(r'^add-tag.html$', tag.AddTagView.as_view(), name="add_tag"),

    # 日志管理
    url(r'^error_log.html$', error_log.ErrorLogListView.as_view(), name="error_log_index"),
    url(r'^error_logs.html$', error_log.ErrorLogJsonView.as_view(), name="error_log_json"),
    url(r'^add-error_log.html$', error_log.AddErrorLogView.as_view(), name="add_error_log"),
]
