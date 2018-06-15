// 获取时间函数
function settime(){
    // var date = new Date();
    // var year=date.getFullYear();
    // var month=date.getMonth() + 1;
    // if (month >= 1 && month <= 9) {
    //     month = "0" + month;
    // };
    // var day=date.getDate();
    // if (day >= 0 && day <= 9) {
    //     day = "0" + day;
    // };
    // var hour=date.getHours();
    // if (hour >= 0 && hour <= 9) {
    //     hour = "0" + hour;
    // };
    // var minute=date.getMinutes();
    // if (minute >= 0 && minute <= 9) {
    //     minute = "0" + minute;
    // };
    // var second=date.getSeconds();
    // if (second >= 0 && second <= 9) {
    //     second = "0" + second;
    // };
    // $(".main-topRight-time").html(year+"年"+month+"月"+day+"日<span>"+hour+":"+minute+":"+second+"</span>");
    var mydate = new Date()
    var n =mydate.toLocaleString();
    $(".main-topRight-time").html(n);
};



$(function(){
    // 功能栏点击出现与消失
    // $(".leftnav-itemTitle.haveList").click(function(){
    //     $(".leftnav-itemTitle.nolist").removeClass("on");
    //     $(this).next().slideToggle(200);
    //     $(this).toggleClass("on");
    // });
    // $(".leftnav-itemTitle.nolist").click(function(){
    //     $(".leftnav-itemTitle.nolist").removeClass("on");
    //     $(this).addClass("on");
    //     $(".leftnav-itemlist li a").removeClass("on");
    // });
    // $(".leftnav-itemlist li a").click(function(){
    //     $(".leftnav-itemlist li a").removeClass("on");
    //     $(this).addClass("on");
    // });
    // 获取时间
    settime();
    var getTime=setInterval(settime,1000);


    // 小车动画
    // $(".home-state-list").eq(0).click(function(){
    //     $(".che1").eq(0).animate({"opacity":1},1000,function(){
    //         $(".gan").eq(0).animate({"height":"30px"},1200,function(){
    //             $(".che1").eq(0).animate({"left":"450px"},2000,function(){
    //                 $(".gan").eq(0).animate({'height':"115px"},1000);
    //             }).animate({"opacity":0},1000).animate({"left":"-450px"},100,function () {
    //                 $(".che2").eq(0).delay(800).animate({"opacity":1},1000,function(){
    //                     $(".gan1").eq(0).animate({"height":"30px"},1200,function(){
    //                         $(".che2").eq(0).animate({"left":"-500px"},2000,function(){
    //                             $(".gan1").eq(0).animate({'height':"115px"},1000);
    //                         }).animate({"opacity":0},1000).animate({"left":"450px"},100);
    //                     });
    //                 });
    //             });
    //         });
    //     });
    // });
    // $(".home-state-list").eq(1).click(function(){
    //     $(".che1").eq(1).animate({"opacity":1},1000,function(){
    //         $(".gan").eq(1).animate({"height":"30px"},1200,function(){
    //             $(".che1").eq(1).animate({"left":"450px"},2000,function(){
    //                 $(".gan").eq(1).animate({'height':"115px"},1000);
    //             }).animate({"opacity":0},1000).animate({"left":"-450px"},100,function () {
    //                 $(".che2").eq(1).delay(800).animate({"opacity":1},1000,function(){
    //                     $(".gan1").eq(1).animate({"height":"30px"},1200,function(){
    //                         $(".che2").eq(1).animate({"left":"-500px"},2000,function(){
    //                             $(".gan1").eq(1).animate({'height':"115px"},1000);
    //                         }).animate({"opacity":0},1000).animate({"left":"450px"},100);
    //                     });
    //                 });
    //             });
    //         });
    //     });
    // });
});