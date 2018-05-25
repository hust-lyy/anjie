$(function(){
    // function animate(){
    //     $(".che1").animate({"opacity":1},1000,function(){
    //         $(".gan").animate({"height":"30px"},1200,function(){
    //             $(".che1").animate({"left":"450px"},2000,function(){
    //                 $(".gan").animate({'height':"115px"},1000);
    //             }).animate({"opacity":0},1000).animate({"left":"-450px"},100,function () {
    //                 $(".che2").delay(800).animate({"opacity":1},1000,function(){
    //                     $(".gan1").animate({"height":"30px"},1200,function(){
    //                         $(".che2").animate({"left":"-500px"},2000,function(){
    //                             $(".gan1").animate({'height':"115px"},1000);
    //                         }).animate({"opacity":0},1000).animate({"left":"450px"},100);
    //                     });
    //                 });
    //             });
    //         });
    //     });
    // };
    // animate();
    // setInterval(function(){
    //     animate()
    // },20000);

    $(".home-state-list").eq(0).click(function(){
        $(".che1").eq(0).animate({"opacity":1},1000,function(){
            $(".gan").eq(0).animate({"height":"30px"},1200,function(){
                $(".che1").eq(0).animate({"left":"450px"},2000,function(){
                    $(".gan").eq(0).animate({'height':"115px"},1000);
                }).animate({"opacity":0},1000).animate({"left":"-450px"},100,function () {
                    $(".che2").eq(0).delay(800).animate({"opacity":1},1000,function(){
                        $(".gan1").eq(0).animate({"height":"30px"},1200,function(){
                            $(".che2").eq(0).animate({"left":"-500px"},2000,function(){
                                $(".gan1").eq(0).animate({'height':"115px"},1000);
                            }).animate({"opacity":0},1000).animate({"left":"450px"},100);
                        });
                    });
                });
            });
        });
    });
    $(".home-state-list").eq(1).click(function(){
        $(".che1").eq(1).animate({"opacity":1},1000,function(){
            $(".gan").eq(1).animate({"height":"30px"},1200,function(){
                $(".che1").eq(1).animate({"left":"450px"},2000,function(){
                    $(".gan").eq(1).animate({'height':"115px"},1000);
                }).animate({"opacity":0},1000).animate({"left":"-450px"},100,function () {
                    $(".che2").eq(1).delay(800).animate({"opacity":1},1000,function(){
                        $(".gan1").eq(1).animate({"height":"30px"},1200,function(){
                            $(".che2").eq(1).animate({"left":"-500px"},2000,function(){
                                $(".gan1").eq(1).animate({'height':"115px"},1000);
                            }).animate({"opacity":0},1000).animate({"left":"450px"},100);
                        });
                    });
                });
            });
        });
    });
});