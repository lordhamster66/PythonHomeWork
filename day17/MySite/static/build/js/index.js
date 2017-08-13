/**
 * Created by Administrator on 2017/8/13.
 */
// 左侧菜单切换
$("[effect='menu']").click(function () {
    $(this).children(".fright").text("-").parent().siblings().removeClass("hide").parent().siblings().children("[effect='menu']").children(".fright").text("+").parent().siblings().addClass("hide")
});


// 返回顶部
$("#gotop").click(function () {
    $(".admin-body").scrollTop(0);
});


// 添加功能
$(":button[value='添加']").click(function () {
    $("#myModal .modal-title").text("添加");
    $("#myModal .my-modal-content [name='host_id']").text("");
    $("#myModal #confirm").text("确定").attr("target", "insert");
    $("#myModal .my-modal-content #hostname").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #ip").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #port").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #line_status").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #server_style").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #cpu").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #memory").val("").attr("placeholder", "");
    $("#myModal .my-modal-content #disk").val("").attr("placeholder", "");
});


// 全选功能
$(":button[value='全选']").click(function () {
    $("#tb1 :checkbox").prop("checked", true)
});


// 取消功能
$(":button[value='取消']").click(function () {
    $("#tb1 :checkbox").prop("checked", false)
});


// 反选功能
$(":button[value='反选']").click(function () {
    $("#tb1 :checkbox").each(function () {
        if ($(this).prop("checked")) {
            $(this).prop("checked", false)
        } else {
            $(this).prop("checked", true)
        }
    })
});


// 编辑功能
$("#tb1").delegate(".edit", "click", function () {
    $("#myModal .modal-title").text("编辑");
    var host_id = $(this).parent().siblings("#host_id").text();
    $("#myModal .my-modal-content [name='host_id']").text(host_id);
    $("#myModal #confirm").text("修改").attr("target", "update");
    $.post('/select/',
        {"host_id": host_id},
        function (e) {
            host_obj = JSON.parse(e); //由JSON字符串转换为JSON对象
            $("#myModal .my-modal-content #hostname").val(host_obj.hostname);
            $("#myModal .my-modal-content #ip").val(host_obj.ip);
            $("#myModal .my-modal-content #port").val(host_obj.port);
            $("#myModal .my-modal-content #line_status").val(host_obj.line_status);
            $("#myModal .my-modal-content #server_style").val(host_obj.server_style);
            $("#myModal .my-modal-content #cpu").val(host_obj.cpu);
            $("#myModal .my-modal-content #memory").val(host_obj.memory);
            $("#myModal .my-modal-content #disk").val(host_obj.disk);
        }
    )
});


// 查看详细信息功能
$("#tb1").delegate(".detail", "click", function () {
    $("#myModal1 .modal-title").text("详细信息");
    var host_id = $(this).parent().siblings("#host_id").text();
    $("#myModal1 .my-modal-content [name='host_id']").text(host_id);
    $.post('/select/',
        {"host_id": host_id},
        function (e) {
            host_obj = JSON.parse(e); //由JSON字符串转换为JSON对象
            $("#myModal1 .my-modal-content [name='hostname']").text(host_obj.hostname);
            $("#myModal1 .my-modal-content [name='ip']").text(host_obj.ip);
            $("#myModal1 .my-modal-content [name='port']").text(host_obj.port);
            $("#myModal1 .my-modal-content [name='line_status']").text(host_obj.line_status);
            $("#myModal1 .my-modal-content [name='server_style']").text(host_obj.server_style);
            $("#myModal1 .my-modal-content [name='cpu']").text(host_obj.cpu);
            $("#myModal1 .my-modal-content [name='memory']").text(host_obj.memory);
            $("#myModal1 .my-modal-content [name='disk']").text(host_obj.disk);
        }
    )
});


// 修改主机信息
$("#myModal").delegate("[target='update']", "click", function () {
    var host_id = $(this).parent().siblings().find("[name='host_id']").text();
    var hostname = $(this).parent().siblings().find("#hostname").val();
    var ip = $(this).parent().siblings().find("#ip").val();
    var port = $(this).parent().siblings().find("#port").val();
    var line_status = $(this).parent().siblings().find("#line_status").val();
    var server_style = $(this).parent().siblings().find("#server_style").val();
    var cpu = $(this).parent().siblings().find("#cpu").val();
    var memory = $(this).parent().siblings().find("#memory").val();
    var disk = $(this).parent().siblings().find("#disk").val();
    host_info = {
        "host_id": host_id, "hostname": hostname, "ip": ip, "port": port, "line_status": line_status,
        "server_style": server_style, "cpu": cpu, "memory": memory, "disk": disk
    };
    host_info = JSON.stringify(host_info);
    $.post('/update/',
        {"host_info": host_info},
        function (e) {
            if (e == "ok") {
                window.location.reload();//刷新当前页面.
            }
        }
    )
});


// 添加主机
$("#myModal").delegate("[target='insert']", "click", function () {
    var flag = true;  //
    $(this).parent().siblings().find("#hostname,#ip,#port,#line_status,#server_style,#cpu,#memory,#disk").each(function () {
        if ($(this).val().length == 0) {
            $(this).attr("placeholder", "不能为空！");
            flag = false;
            return false
        }
    });
    if (flag) {
        var hostname = $(this).parent().siblings().find("#hostname").val();
        var ip = $(this).parent().siblings().find("#ip").val();
        var port = $(this).parent().siblings().find("#port").val();
        var line_status = $(this).parent().siblings().find("#line_status").val();
        var server_style = $(this).parent().siblings().find("#server_style").val();
        var cpu = $(this).parent().siblings().find("#cpu").val();
        var memory = $(this).parent().siblings().find("#memory").val();
        var disk = $(this).parent().siblings().find("#disk").val();
        host_info = {
            "hostname": hostname, "ip": ip, "port": port, "line_status": line_status,
            "server_style": server_style, "cpu": cpu, "memory": memory, "disk": disk
        };
        host_info = JSON.stringify(host_info);
        var username = $("#username").attr("target");
        $.post('/insert/',
            {"host_info": host_info, "username": username},
            function (e) {
                ret = JSON.parse(e);
                if (ret.HostName) {
                    $("#myModal").find("#hostname").val("").attr("placeholder", "主机名已经存在！请重新输入!");
                } else if (ret.IP) {
                    $("#myModal").find("#ip").val("").attr("placeholder", "主机地址已经存在！请重新输入!");
                } else if (ret.Confirm) {
                    window.location.reload();//刷新当前页面.
                }
            }
        )
    } else {
        return false
    }
});


// 删除功能
$("#tb1").delegate(".delete", "click", function () {
    var host_id = $(this).parent().siblings("#host_id").text();
    $("#myModal2 #delete").attr("target", host_id);
});


// 删除主机
$("#myModal2").delegate("#delete", "click", function () {
    var host_id = $(this).attr("target");
    $.post('/delete/',
        {"host_id": host_id},
        function (e) {
            if (e == "ok") {
                window.location.reload();//刷新当前页面.
            }
        }
    )
});