(function (jq) {
    jq.extend({
            // 初始化复选框功能
            'initFilterHorizontal': function (url, href_url) {
                // 双击移动选项
                $(".filter_horizontal").delegate("[tag='option']", "dblclick", function () {
                    var field_name = $(this).parent().attr("field_name");  // 获取字段名
                    var move_to_id = field_name + "_move_to";
                    var move_from_id = field_name + "_move_from";
                    var move_dict = {};
                    move_dict[move_to_id] = move_from_id;
                    move_dict[move_from_id] = move_to_id;
                    if ($(this).parent().children().length == 1) {
                        $(this).parents(".panel").next().children("a").removeClass("active");
                    }
                    var current_ele = $(this);  // 当前标签
                    var parent_ele_id = $(this).parent().attr("id"); // 当前标签的父标签ID
                    $(this).remove();  // 移除该标签
                    $("#" + move_dict[parent_ele_id]).append(current_ele).parents(".panel").next().children("a").addClass("active");  // 移动选择的标签
                    $("#" + field_name + "_add_link").removeClass("active");
                    $("#" + field_name + "_remove_link").removeClass("active");
                });
                // 提交form表单之前自动全选复选框右边的所有选项
                $("#submit").click(function () {
                    $(".move_to").children().each(function () {
                        $(this).prop("selected", true);  // 将用户移动到已选择框中的选项全部选中
                    });
                    $("#base-form").find(":disabled").removeAttr("disabled");
                    $.post(url, $("#base-form").serialize(), function (obj) {
                        console.log(obj);
                        if (obj.status) {
                            location.href = href_url;
                        } else {
                            var error_msg = "";
                            for (var i in obj.error) {
                                error_msg += i + ":   " + obj.error[i] + "\n";
                            }
                            swal("Ops!", error_msg, "warning");
                        }
                    })
                });
                // 全选和删除全部选项
                $(".add_all_link").click(function () {
                    var field_name = $(this).parent().prev().children().find("select").attr("field_name");  // 获取字段名
                    var move_to_id = field_name + "_move_to";
                    var move_from_id = field_name + "_move_from";
                    var move_dict = {};
                    move_dict[move_to_id] = move_from_id;
                    move_dict[move_from_id] = move_to_id;
                    if ($(this).hasClass("active")) {
                        var select_id = $(this).parent().prev().children().find(".filter_horizontal").attr("id");
                        $("#" + move_dict[select_id]).append($(this).parent().prev().children().find("[tag='option']")).parent().parent().next().children("a").addClass("active");  // 移动选择的标签
                        $(this).removeClass("active");
                        $("#" + field_name + "_add_link").removeClass("active");
                        $("#" + field_name + "_remove_link").removeClass("active");
                    }
                });
                // 单击选项
                $(".filter_horizontal").delegate("[tag='option']", "click", function () {
                    var field_name = $(this).parent().attr("field_name");  // 获取字段名
                    var move_to_id = field_name + "_move_to";
                    var move_from_id = field_name + "_move_from";
                    var move_link_dict = {};
                    move_link_dict[move_from_id] = field_name + "_add_link";
                    move_link_dict[move_to_id] = field_name + "_remove_link";
                    var parent_ele_id = $(this).parent().attr("id"); // 当前标签的父标签ID
                    $("#" + move_link_dict[parent_ele_id]).addClass("active");
                });
                // 右移动选项
                $(".selector-add").click(function () {
                    var field_name = $(this).attr("field_name");  // 获取字段名
                    if ($(this).hasClass("active")) {
                        $("#" + field_name + "_move_to").append($("#" + field_name + "_move_from").children(":selected"));
                        $(this).removeClass("active");
                        $("#" + field_name + "_remove_link").removeClass("active");
                        $("#" + field_name + "_clearall").addClass("active");
                        if ($("#" + field_name + "_move_from").children().length == 0) {
                            $("#" + field_name + "_chooseall").removeClass("active");
                        }
                    }
                });
                //左移动选项
                $(".selector-remove").click(function () {
                    var field_name = $(this).attr("field_name");  // 获取字段名
                    if ($(this).hasClass("active")) {
                        $("#" + field_name + "_move_from").append($("#" + field_name + "_move_to").children(":selected"));
                        $(this).removeClass("active");
                        $("#" + field_name + "_add_link").removeClass("active");
                        $("#" + field_name + "_chooseall").addClass("active");
                        if ($("#" + field_name + "_move_to").children().length == 0) {
                            $("#" + field_name + "_clearall").removeClass("active");
                        }
                    }
                });
            }
        }
    );
})(jQuery);