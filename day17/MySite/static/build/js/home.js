/**
 * Created by Administrator on 2017/8/13.
 */
// 重定向至登录页面
$("#login").click(function () {
   window.location.href="/login/";
});


// 初始化数据库
$("#init-db").click(function () {
   $.get("/init/", function (e) {
       if(e == "done!"){
           alert("成功！")
       }else{
           alert("失败！")
       }
   })
});


// 重置数据库
$("#drop-db").click(function () {
   $.get("/drop/", function (e) {
       if(e == "done!"){
           alert("成功！")
       }else{
           alert("失败！")
       }
   })
});
