// var home_Path = document.location.protocol +'//' + window.document.location.hostname +'/';

var userAgent = window.navigator.userAgent.toLowerCase();
//console.log(userAgent);
var norunAI = [
  "android",
  "iphone",
  "ipod",
  "ipad",
  "windows phone",
  "mqqbrowser",
  "msie",
  "trident/7.0"
];
var norunFlag = false;

for (var i = 0; i < norunAI.length; i++) {
  if (userAgent.indexOf(norunAI[i]) > -1) {
    norunFlag = true;
    break;
  }
}

if (!window.WebGLRenderingContext) {
  norunFlag = true;
}

if (!norunFlag) {
  var hitFlag = false;
  var AIFadeFlag = false;
  var liveTlakTimer = null;
  var sleepTimer_ = null;
  var AITalkFlag = false;
  var talkNum = 0;
  (function () {
    function renderTip(template, context) {
      var tokenReg = /(\\)?\{([^\{\}\\]+)(\\)?\}/g;
      return template.replace(tokenReg, function (word, slash1, token, slash2) {
        if (slash1 || slash2) {
          return word.replace("\\", "");
        }
        var variables = token.replace(/\s/g, "").split(".");
        var currentObject = context;
        var i, length, variable;
        for (i = 0, length = variables.length; i < length; ++i) {
          variable = variables[i];
          currentObject = currentObject[variable];
          if (currentObject === undefined || currentObject === null) return "";
        }
        return currentObject;
      });
    }

    String.prototype.renderTip = function (context) {
      return renderTip(this, context);
    };

    var re = /x/;
    re.toString = function () {
      showMessage("哈哈，你打开了控制台，是想要看看我的秘密吗？", 5000);
      return "";
    };

    jQuery(document).on("copy", function () {
      showMessage("你都复制了些什么呀，转载要记得加上出处哦~~", 5000);
    });

    function initTips() {
      jQuery.ajax({
        cache: true,
        url: message_Path + "message.json",
        dataType: "json",
        success: function (result) {
          jQuery.each(result.mouseover, function (index, tips) {
            jQuery(tips.selector).mouseover(function () {
              var text = tips.text;
              if (Array.isArray(tips.text))
                text =
                  tips.text[
                  Math.floor(Math.random() * tips.text.length + 1) - 1
                  ];
              text = text.renderTip({ text: jQuery(this).text() });
              showMessage(text, 3000);
              talkValTimer();
              clearInterval(liveTlakTimer);
              liveTlakTimer = null;
            });
            jQuery(tips.selector).mouseout(function () {
              //showHitokoto();
              if (liveTlakTimer == null) {
                liveTlakTimer = window.setInterval(function () {
                  // showHitokoto();
                }, 15000);
              }
            });
          });
          jQuery.each(result.click, function (index, tips) {
            jQuery(tips.selector).click(function () {
              if (hitFlag) {
                return false;
              }
              hitFlag = true;
              setTimeout(function () {
                hitFlag = false;
              }, 8000);
              var text = tips.text;
              if (Array.isArray(tips.text))
                text =
                  tips.text[
                  Math.floor(Math.random() * tips.text.length + 1) - 1
                  ];
              text = text.renderTip({ text: jQuery(this).text() });
              showMessage(text, 3000);
            });
            clearInterval(liveTlakTimer);
            liveTlakTimer = null;
            if (liveTlakTimer == null) {
              liveTlakTimer = window.setInterval(function () {
                //showHitokoto();
              }, 15000);
            }
          });
        }
      });
    }
    initTips();

    var text;
    if (document.referrer !== "") {
      var referrer = document.createElement("a");
      referrer.href = document.referrer;
      text =
        '嗨！来自 <span style="color:#0099cc;">' +
        referrer.hostname +
        "</span> 的朋友！";
      var domain = referrer.hostname.split(".")[1];
      if (domain == "baidu") {
        text =
          '嗨！ 来自 百度搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' +
          document.title.split(" - ")[0] +
          " 」</span>";
      } else if (domain == "so") {
        text =
          '嗨！ 来自 360搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' +
          document.title.split(" - ")[0] +
          " 」</span>";
      } else if (domain == "google") {
        text =
          '嗨！ 来自 谷歌搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' +
          document.title.split(" - ")[0] +
          " 」</span>";
      }
    } else {
      if (window.location.href == home_Path) {
        //主页URL判断，需要斜杠结尾
        var now = new Date().getHours();
        if (now > 23 || now <= 5) {
          text = "你是夜猫子呀？这么晚还不睡觉，明天起的来嘛？";
        } else if (now > 5 && now <= 7) {
          text = "早上好！一日之计在于晨，美好的一天就要开始了！";
        } else if (now > 7 && now <= 11) {
          text = "上午好！工作顺利嘛，不要久坐，多起来走动走动哦！";
        } else if (now > 11 && now <= 14) {
          text = "中午了，工作了一个上午，现在是午餐时间！";
        } else if (now > 14 && now <= 17) {
          text = "午后很容易犯困呢，今天的运动目标完成了吗？";
        } else if (now > 17 && now <= 19) {
          text = "傍晚了！窗外夕阳的景色很美丽呢，最美不过夕阳红~~";
        } else if (now > 19 && now <= 21) {
          text = "晚上好，今天过得怎么样？";
        } else if (now > 21 && now <= 23) {
          text = "已经这么晚了呀，早点休息吧，晚安~~";
        } else {
          text = "嗨~ 快来逗我玩吧！";
        }
      } else {
        text =
          '欢迎阅读<span style="color:#0099cc;">「 ' +
          document.title.split(" - ")[0] +
          " 」</span>";
      }
    }
    showMessage(text, 12000);
  })();

  liveTlakTimer = setInterval(function () {
    //showHitokoto();
  }, 15000);

  /*function showHitokoto() {
    if (sessionStorage.getItem("Sleepy") !== "1") {
      if (!AITalkFlag) {
        jQuery.getJSON("https://sslapi.hitokoto.cn/", function(result) {
          talkValTimer();
          showMessage(result.hitokoto, 0);
        });
      }
    } else {
      hideMessage(0);
      if (sleepTimer_ == null) {
        sleepTimer_ = setInterval(function() {
          checkSleep();
        }, 200);
      }
      console.log(sleepTimer_);
    }
  }*/

  function checkSleep() {
    var sleepStatu = sessionStorage.getItem("Sleepy");
    if (sleepStatu !== "1") {
      talkValTimer();
      showMessage("你回来啦~", 0);
      clearInterval(sleepTimer_);
      sleepTimer_ = null;
    }
  }

  function showMessage(text, timeout) {
    if (Array.isArray(text))
      text = text[Math.floor(Math.random() * text.length + 1) - 1];
    //console.log('showMessage', text);
    jQuery(".message").stop();
    jQuery(".message").html(text);
    jQuery(".message").fadeTo(200, 1);
    //if (timeout === null) timeout = 5000;
    //hideMessage(timeout);
  }
  function talkValTimer() {
    jQuery("#live_talk").val("1");
  }

  function hideMessage(timeout) {
    //jQuery('.message').stop().css('opacity',1);
    if (timeout === null) timeout = 5000;
    jQuery(".message")
      .delay(timeout)
      .fadeTo(200, 0);
  }

  function initLive2d() {
    jQuery("#hideButton").on("click", function () {
      if (AIFadeFlag) {
        return false;
      } else {
        AIFadeFlag = true;
        localStorage.setItem("live2dhidden", "0");
        jQuery("#landlord").fadeOut(200);
        jQuery("#open_live2d")
          .delay(200)
          .fadeIn(200);
        setTimeout(function () {
          AIFadeFlag = false;
        }, 300);
      }
    });
    jQuery("#open_live2d").on("click", function () {
      if (AIFadeFlag) {
        return false;
      } else {
        AIFadeFlag = true;
        localStorage.setItem("live2dhidden", "1");
        jQuery("#open_live2d").fadeOut(200);
        jQuery("#landlord")
          .delay(200)
          .fadeIn(200);
        setTimeout(function () {
          AIFadeFlag = false;
        }, 300);
      }
    });
    jQuery("#youduButton").on("click", function () {
      if (jQuery("#youduButton").hasClass("doudong")) {
        var typeIs = jQuery("#youduButton").attr("data-type");
        jQuery("#youduButton").removeClass("doudong");
        jQuery("body").removeClass(typeIs);
        jQuery("#youduButton").attr("data-type", "");
        // jQuery("#landlord").removeAttr("style").fadeIn();
      } else {
        var duType = jQuery("#duType").val();
        var duArr = duType.split(",");
        var dataType = duArr[Math.floor(Math.random() * duArr.length)];

        jQuery("#youduButton").addClass("doudong");
        jQuery("#youduButton").attr("data-type", dataType);
        jQuery("body").addClass(dataType);
        //jQuery("#landlord").removeAttr("style").css({
        //top: jQuery(window).scrollTop() + 137 + "px"
        //});
      }
    });
    if (talkAPI !== "") {
      jQuery("#showInfoBtn").on("click", function () {
        var live_statu = jQuery("#live_statu_val").val();
        if (live_statu == "0") {
          return;
        } else {
          jQuery("#live_statu_val").val("0");
          jQuery(".live_talk_input_body").fadeOut(500);
          AITalkFlag = false;
          //showHitokoto();
          jQuery("#showTalkBtn").show();
          jQuery("#showInfoBtn").hide();
        }
      });
      jQuery("#showTalkBtn").on("click", function () {
        var live_statu = jQuery("#live_statu_val").val();
        if (live_statu == "1") {
          return;
        } else {
          jQuery("#live_statu_val").val("1");
          jQuery(".live_talk_input_body").fadeIn(500);
          AITalkFlag = true;
          jQuery("#showTalkBtn").hide();
          jQuery("#showInfoBtn").show();
        }
      });
      jQuery("#talk_send").on("click", function () {
        var info_ = jQuery("#AIuserText").val();
        var userid_ = jQuery("#AIuserName").val();
        if (info_ == "") {
          showMessage("写点什么吧！", 0);
          return;
        }
        if (userid_ == "") {
          showMessage("聊之前请告诉我你的名字吧！", 0);
          return;
        }
        showMessage("思考中~", 0);
        jQuery.ajax({
          type: "POST",
          url: talkAPI,
          data: {
            info: info_,
            userid: userid_
          },
          success: function (res) {
            if (res.code !== 100000) {
              talkValTimer();
              showMessage("似乎有什么错误，请和站长联系！", 0);
            } else {
              talkValTimer();
              showMessage(res.text, 0);
            }
            console.log(res);
            jQuery("#AIuserText").val("");
            sessionStorage.setItem("live2duser", userid_);
          }
        });
      });
    } else {
      jQuery("#showInfoBtn").hide();
      jQuery("#showTalkBtn").hide();
    }
    //获取音乐信息初始化
    var bgmListInfo = jQuery("input[name=live2dBGM]");
    if (bgmListInfo.length == 0) {
      jQuery("#musicButton").hide();
    } else {
      var bgmPlayNow = parseInt(jQuery("#live2d_bgm").attr("data-bgm"));
      var bgmPlayTime = 0;
      var live2dBGM_Num = sessionStorage.getItem("live2dBGM_Num");
      var live2dBGM_PlayTime = sessionStorage.getItem("live2dBGM_PlayTime");
      if (live2dBGM_Num) {
        if (live2dBGM_Num <= jQuery("input[name=live2dBGM]").length - 1) {
          bgmPlayNow = parseInt(live2dBGM_Num);
        }
      }
      if (live2dBGM_PlayTime) {
        bgmPlayTime = parseInt(live2dBGM_PlayTime);
      }
      var live2dBGMSrc = bgmListInfo.eq(bgmPlayNow).val();
      jQuery("#live2d_bgm").attr("data-bgm", bgmPlayNow);
      jQuery("#live2d_bgm").attr("src", live2dBGMSrc);
      jQuery("#live2d_bgm")[0].currentTime = bgmPlayTime;
      jQuery("#live2d_bgm")[0].volume = 0.5;
      var live2dBGM_IsPlay = sessionStorage.getItem("live2dBGM_IsPlay");
      var live2dBGM_WindowClose = sessionStorage.getItem(
        "live2dBGM_WindowClose"
      );
      if (live2dBGM_IsPlay == "0" && live2dBGM_WindowClose == "0") {
        jQuery("#live2d_bgm")[0].play();
        jQuery("#musicButton").addClass("play");
      }
      sessionStorage.setItem("live2dBGM_WindowClose", "1");
      jQuery("#musicButton").on("click", function () {
        if (jQuery("#musicButton").hasClass("play")) {
          jQuery("#live2d_bgm")[0].pause();
          jQuery("#musicButton").removeClass("play");
          sessionStorage.setItem("live2dBGM_IsPlay", "1");
        } else {
          jQuery("#live2d_bgm")[0].play();
          jQuery("#musicButton").addClass("play");
          sessionStorage.setItem("live2dBGM_IsPlay", "0");
        }
      });
      window.onbeforeunload = function () {
        sessionStorage.setItem("live2dBGM_WindowClose", "0");
        if (jQuery("#musicButton").hasClass("play")) {
          sessionStorage.setItem("live2dBGM_IsPlay", "0");
        }
      };
      document
        .getElementById("live2d_bgm")
        .addEventListener("timeupdate", function () {
          var live2dBgmPlayTimeNow = document.getElementById("live2d_bgm")
            .currentTime;
          sessionStorage.setItem("live2dBGM_PlayTime", live2dBgmPlayTimeNow);
        });
      document
        .getElementById("live2d_bgm")
        .addEventListener("ended", function () {
          var listNow = parseInt(jQuery("#live2d_bgm").attr("data-bgm"));
          listNow++;
          if (listNow > jQuery("input[name=live2dBGM]").length - 1) {
            listNow = 0;
          }
          var listNewSrc = jQuery("input[name=live2dBGM]")
            .eq(listNow)
            .val();
          sessionStorage.setItem("live2dBGM_Num", listNow);
          jQuery("#live2d_bgm").attr("src", listNewSrc);
          jQuery("#live2d_bgm")[0].play();
          jQuery("#live2d_bgm").attr("data-bgm", listNow);
        });
      document
        .getElementById("live2d_bgm")
        .addEventListener("error", function () {
          jQuery("#live2d_bgm")[0].pause();
          jQuery("#musicButton").removeClass("play");
          showMessage("音乐似乎加载不出来了呢！", 0);
        });
    }
    //获取用户名
    var live2dUser = sessionStorage.getItem("live2duser");
    if (live2dUser !== null) {
      jQuery("#AIuserName").val(live2dUser);
    }
    //获取位置
    var landL = sessionStorage.getItem("historywidth");
    var landB = sessionStorage.getItem("historyheight");
    if (landL == null || landB == null) {
      landL = "5px";
      landB = "0px";
    }
    jQuery("#live2d").css("left", landL + "px");
    jQuery("#live2d").css("bottom", landB + "px");
    //移动
    function getEvent() {
      return window.event || arguments.callee.caller.arguments[0];
    }
    var smcc = document.getElementById("landlord");
    var moveX = 0;
    var moveY = 0;
    var moveBottom = 0;
    var moveLeft = 0;
    var moveable = false;
    var docMouseMoveEvent = document.onmousemove;
    var docMouseUpEvent = document.onmouseup;
    smcc.onmousedown = function () {
      var ent = getEvent();
      moveable = true;
      moveX = ent.clientX;
      moveY = ent.clientY;
      var obj = smcc;
      moveBottom = parseInt(obj.style.bottom);
      moveLeft = parseInt(obj.style.left);
      if ((isFirefox = navigator.userAgent.indexOf("Firefox") > 0)) {
        window.getSelection().removeAllRanges();
      }
      document.onmousemove = function () {
        if (moveable) {
          var ent = getEvent();
          var x = moveLeft + ent.clientX - moveX;
          var y = moveBottom + (moveY - ent.clientY);
          obj.style.left = x + "px";
          obj.style.bottom = y + "px";
        }
      };
      document.onmouseup = function () {
        if (moveable) {
          var historywidth = obj.style.left;
          var historyheight = obj.style.bottom;
          historywidth = historywidth.replace("px", "");
          historyheight = historyheight.replace("px", "");
          sessionStorage.setItem("historywidth", historywidth);
          sessionStorage.setItem("historyheight", historyheight);
          document.onmousemove = docMouseMoveEvent;
          document.onmouseup = docMouseUpEvent;
          moveable = false;
          moveX = 0;
          moveY = 0;
          moveBottom = 0;
          moveLeft = 0;
        }
      };
    };
  }
  jQuery(document).ready(function () {
    var AIimgSrc = model_textures;
    var images = [];
    var imgLength = AIimgSrc.length;
    var loadingNum = 0;
    for (var i = 0; i < imgLength; i++) {
      images[i] = new Image();
      images[i].src = model_Path + AIimgSrc[i];
      images[i].onload = function () {
        loadingNum++;
        if (loadingNum === imgLength) {
          var live2dhidden = localStorage.getItem("live2dhidden");
          if (live2dhidden === "0") {
            setTimeout(function () {
              jQuery("#open_live2d").fadeIn(200);
            }, 1300);
          } else {
            setTimeout(function () {
              jQuery("#landlord").fadeIn(200);
            }, 1300);
          }
          setTimeout(function () {
            loadlive2d("live2d", model_Path + "model/model.json");
          }, 300);
          initLive2d();
          images = null;
        }
      };
    }
  });
}
