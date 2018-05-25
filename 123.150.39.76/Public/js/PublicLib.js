var curCountDownSMS = 60;
var intervalSMS;
function sendsmsOnclick(target){
	var mobile = $('#mobile').val();
	if (!mobile.match(/^\d{11}$/)){
		errorAlert("请输入正确的手机号码");
		return;
	}		
	
	$("#sendsms").attr("disabled", true);
	curCountDownSMS = 60;
	$("#sendsms").html("重发("+curCountDownSMS+")");
	intervalSMS = setInterval(countDownSMS, "1000");
	
	var url = __JSROOT__ + "/index.php/Home/Member/Public/sendSMS";
	if (target=="forgetpasswd"){
		url = __JSROOT__ + "/index.php/Home/Member/Public/sendPasswdSMS";
	}
	$.get(url,
			{
				mobile: mobile,
		    },
		    function(data,status){
		    	var dataArr = data.split("###");
		    	var realInfo = dataArr[1];
		    	var infoArr = realInfo.split("#@#");
		    	if (infoArr[0] == "0"){
		    		errorAlert(infoArr[1]);
		    		clearTimeout(intervalSMS);
		    		$("#sendsms").html("发送密码");
		    		$("#sendsms").attr("disabled", false);
		    	}
		    	else{
		    		infoAlert("手机验证码为:" + infoArr[1]);
		    	}
		    	
		    	//var authCode = data.substring(data.length-4);
				//$('#smsAuthCode').val(authCode);					
			}
	);
}
/**
 * 点击发送验证码以后倒计时
 */
function countDownSMS(){
	curCountDownSMS--;
	$("#sendsms").html("重发("+curCountDownSMS+")");
	if (curCountDownSMS == 0){
		clearTimeout(intervalSMS);
		$("#sendsms").html("发送密码");
		$("#sendsms").attr("disabled", false);
	}
}

function successAlert(msg){
	bootbox.dialog({
        message: msg,
        title: "操作成功",
        buttons: {
          danger: {
            label: "知道了",
            className: "green"
          }
        }
    });
}
function errorAlert(msg){
	bootbox.dialog({
        message: msg,
        title: "错误信息",
        buttons: {
          danger: {
            label: "知道了",
            className: "red"
          }
        }
    });
}
function infoAlert(msg){
	bootbox.dialog({
        message: msg,
        title: "提示信息",
        buttons: {
          danger: {
            label: "知道了",
            className: "blue"
          }
        }
    });
}
function confirmBox(msg){
	bootbox.confirm(msg);
}