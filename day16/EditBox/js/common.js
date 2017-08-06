/**
 * Created by Administrator on 2017/8/5.
 */


// 全选功能
$(".menu input[value='全选']").click(function () {
    $("#table1 :checkbox").prop("checked", true);
    if ($(".edit").hasClass("editing")) {       // 编辑状态下处理方法
        $("#table1").children().each(function () {  // 循环每一行
            var flag = $(this).children(":eq(1)").children(":eq(0)").is("input");
            if (flag) {
            } else {                  // 只有不是编辑形态才会进行形态切换
                editRow(this);
            }
        })
    }
});


// 取消功能
$(".menu input[value='取消']").click(function () {
    $("#table1 :checkbox").prop("checked", false);
    if ($(".edit").hasClass("editing")) {       // 编辑状态下处理方法
        $("#table1").children().each(function () {  // 循环每一行
            var flag = $(this).children(":eq(1)").children(":eq(0)").is("input");
            if (flag) {               // 是编辑形态下才会切换为非编辑形态
                uneditRow(this);
            }
        })
    }
});


// 反选功能
$(".menu input[value='反选']").click(function () {
    $("#table1 :checkbox").each(function () {
        $(this).prop("checked", $(this).prop("checked") ? false : true);
    });
    if ($(".edit").hasClass("editing")) {       // 编辑状态下处理方法
        $("#table1").children().each(function () {  // 循环每一行
            var flag = $(this).children(":eq(1)").children(":eq(0)").is("input");
            if (flag) {                // 编辑形态则切换为非编辑形态
                uneditRow(this);
            } else {                   // 非编辑形态则切换为编辑形态
                editRow(this);
            }
        })
    }
});


// 进入和取消编辑模式功能
$(".edit").click(function () {
    $(this).toggleClass("editing");   // 编辑和非编辑状态自由切换
    var edit_flag = $(this).hasClass("editing");   // 获取是否是编辑状态
    $("#table1").children().each(function () {     // 循环表格的每一行
        if ($(this).find(":checkbox").prop("checked")) {  // 判断checkbox是否被选中
            if (edit_flag) {                         // 是编辑状态
                editRow(this);
            } else {                                 // 不是编辑状态
                uneditRow(this);
            }
        }
    })
});


// 切换编辑形态功能
function editRow(self) {
    $(self).children().eq(0).nextUntil(".line-or-not").each(function () {  // 循环不是状态的每个单元格
        var info = $(this).text();  // 获取该单元格的信息
        $(this).html("<input type='text' value='" + info + "'>");  // 更改单元格内容
    });
    var select_tag = document.createElement("select");  // 创建一个select标签
    var option_tag1 = document.createElement("option");  // 创建一个option标签
    var option_tag2 = document.createElement("option");
    $(select_tag).attr("name", "status");
    $(option_tag1).text("在线").attr("value", "在线");  // 给option标签设置内容
    $(option_tag2).text("下线").attr("value", "下线");
    $(select_tag).append(option_tag1).append(option_tag2);  // 将option标签放入select标签
    var option_selected = $(self).children(".line-or-not").text();  // 获取当前的选择内容
    $(select_tag).val(option_selected);  // 根据当前选择内容改变select标签的选择状态
    $(self).children(".line-or-not").empty().append(select_tag);  // 将状态单元格的内容替换为select标签
}


// 取消编辑形态功能
function uneditRow(self) {
    $(self).children().eq(0).nextUntil(".line-or-not").each(function () {  // 循环不是状态的每个单元格
        var info = $(this).children(":text").val();  // 获取该单元格的信息
        $(this).html(info);  // 更改单元格内容
    });
    var option_selected = $(self).children(".line-or-not").find("select option:selected").text();  // 获取当前的选择内容
    $(self).children(".line-or-not").empty().text(option_selected);  // 将状态单元格的内容替换为文字
}


// 单个选取切换编辑形态功能
$("#table1 :checkbox").click(function () {
    var flag = $(this).parent().next().children(":eq(0)").is("input");
    if ($(".edit").hasClass("editing")) {       // 是编辑状态
        if ($(this).is(':checked')) {          // 被选中
            if (flag) {
            } else {                           // 非编辑状态才会切换为编辑状态
                editRow($(this).parent().parent()[0]);
            }
        } else {
            if (flag) {                        // 是编辑状态才会切换为非编辑状态
                uneditRow($(this).parent().parent()[0]);
            }
        }
    }
});


// 判断Ctrl是否被按下，被按下则为true,反之为false, 借鉴导师
key_stay = false;
$(document).keyup(function (event) {
    if (event.keyCode == 17) {
        key_stay = false;
    }
});
$(document).keydown(function (event) {
    if (event.keyCode == 17) {
        key_stay = true;
    }
});


// 按住CTRL同时改变状态功能
$("#table1").delegate("select", "click", function () {
        if (key_stay) {
            var info = $(this).children('option:selected').text();
            $("#table1 select").val(info);
        }
    }
);
