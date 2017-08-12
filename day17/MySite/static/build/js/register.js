/**
 * Created by Administrator on 2017/8/11.
 */
$("#btn_register").click(function () {
    var registerObj = new Object();
    registerObj.accountNo = $("#inputAccount").val();
    registerObj.pwd = $("#inputPassword").val();
    registerObj.pwdAgain = $("#inputPasswordAgain").val();
    if($("#inputAccount").val().length == 0){
        $("#accountDiv").addClass("has-error");
        $("#account-error").text("用户名不能为空！");
        $("#accountMsg").removeClass("hidden");

        $("#pwdDiv").removeClass("has-error");
        $("#pwdMsg").addClass("hidden");

        $("#pwdAgainDiv").removeClass("has-error");
        $("#pwdAgainMsg").addClass("hidden");
        return false
    }else if($("#inputPassword").val().length == 0){
        $("#accountDiv").removeClass("has-error");
        $("#accountMsg").addClass("hidden");

        $("#pwdDiv").addClass("has-error");
        $("#pw-error").text("密码不能为空！");
        $("#pwdMsg").removeClass("hidden");

        $("#pwdAgainDiv").removeClass("has-error");
        $("#pwdAgainMsg").addClass("hidden");
        return false
    } else if($("#inputPasswordAgain").val().length == 0){
        $("#accountDiv").removeClass("has-error");
        $("#accountMsg").addClass("hidden");

        $("#pwdDiv").removeClass("has-error");
        $("#pwdMsg").addClass("hidden");

        $("#pwdAgainDiv").addClass("has-error");
        $("#pwAgain-error").text("确定密码不能为空！");
        $("#pwdAgainMsg").removeClass("hidden");
        return false
    }
    else if($("#inputPasswordAgain").val()!=$("#inputPassword").val()){
        $("#accountDiv").removeClass("has-error");
        $("#accountMsg").addClass("hidden");

        $("#pwdDiv").removeClass("has-error");
        $("#pwdMsg").addClass("hidden");

        $("#pwdAgainDiv").addClass("has-error");
        $("#pwAgain-error").text("两次密码不一样！");
        $("#pwdAgainMsg").removeClass("hidden");
        return false
    }
    var registerJson = JSON.stringify(registerObj); //将JSON对象转化为JSON字符
    $.post('/register_check/',
        {"registerObj": registerJson},
        function (e) {
            e = JSON.parse(e); //由JSON字符串转换为JSON对象
            if (e.accountMsg) {
                $("#accountDiv").addClass("has-error");
                $("#account-error").text("用户名已存在");
                $("#accountMsg").removeClass("hidden");

                $("#pwdDiv").removeClass("has-error");
                $("#pwdMsg").addClass("hidden");

                $("#pwdAgainDiv").removeClass("has-error");
                $("#pwdAgainMsg").addClass("hidden");
            }else if (e.pwdMsg) {
                $("#accountDiv").removeClass("has-error");
                $("#accountMsg").addClass("hidden");

                $("#pwdDiv").addClass("has-error");
                $("#pwdMsg").removeClass("hidden");

                $("#pwdAgainDiv").removeClass("has-error");
                $("#pwAgain-error").text("两次密码不一样！");
                $("#pwdAgainMsg").addClass("hidden");
            }else if (e.user) {
                //location.href="/index/";
                $("#registerForm").submit();
            }
        });
});