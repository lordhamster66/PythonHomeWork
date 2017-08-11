/**
 * Created by Administrator on 2017/8/11.
 */
$("#btn_login").click(function () {
    var loginObj = new Object();
    loginObj.accountNo = $("#inputAccount").val();
    loginObj.pwd = $("#inputPassword").val();
    if($("#inputAccount").val().length == 0){
        $("#accountDiv").addClass("has-error");
        $("#account-error").text("用户名不能为空");
        $("#accountMsg").removeClass("hidden");

        $("#pwdDiv").removeClass("has-error");
        $("#pwdMsg").addClass("hidden");
        return false
    }else if($("#inputPassword").val().length == 0){
        $("#accountDiv").removeClass("has-error");
        $("#accountMsg").addClass("hidden");

        $("#pwdDiv").addClass("has-error");
        $("#pw-error").text("密码不能为空");
        $("#pwdMsg").removeClass("hidden");
        return false
    }
    var loginJson = JSON.stringify(loginObj); //将JSON对象转化为JSON字符
    $.post('/login_check/',
        {"loginObj": loginJson},
        function (e) {
            e = JSON.parse(e); //由JSON字符串转换为JSON对象
            if (e.accountMsg) {
                $("#accountDiv").addClass("has-error");
                $("#account-error").text("用户名不存在");
                $("#accountMsg").removeClass("hidden");

                $("#pwdDiv").removeClass("has-error");
                $("#pwdMsg").addClass("hidden");
            } else if (e.pwdMsg) {
                $("#accountDiv").removeClass("has-error");
                $("#accountMsg").addClass("hidden");

                $("#pwdDiv").addClass("has-error");
                $("#pw-error").text("密码错误");
                $("#pwdMsg").removeClass("hidden");
            } else if (e.user) {
                //location.href="main/successLogin.do";
                $("#loginForm").submit();
            }
        });
});