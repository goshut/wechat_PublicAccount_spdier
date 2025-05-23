# coding=utf-8
from lxml import etree
from lxml.html.clean import Cleaner

str1 = """
<!DOCTYPE html>
<html class="
">
  <head>
    <meta name="wechat-enable-text-zoom-em" content="true">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light dark">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0,viewport-fit=cover">
<link rel="shortcut icon" type="image/x-icon" href="//res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico" reportloaderror>
<link rel="mask-icon" href="//res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg" color="#4C4C4C" reportloaderror>
<link rel="apple-touch-icon-precomposed" href="//res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png" reportloaderror>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="format-detection" content="telephone=no">
<meta name="referrer" content="origin-when-cross-origin">
<meta name="referrer" content="strict-origin-when-cross-origin">
<script  nonce="1682091926" reportloaderror>try{document.getElementsByTagName('html').item(0).style.webkitTextSizeAdjust=JSON.parse(window.__wxWebEnv.getEnv()).fontScale+'%'}catch(e){}</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>
  window.logs = { pagetime: {} };
  window.logs.pagetime['html_begin'] = (+new Date());
  window.LANG = "zh_CN"; // 页面语言 zh_CN en_US
</script>

    <script type="text/javascript" nonce="1682091926" reportloaderror>
  /**
   * 于2022-02-21重构vite
   * 仅保留原有moon.js中上报相关的部分
   * @author baakqiu
   * @date 2022-02-21
   */
  
  var WX_BJ_REPORT = window.WX_BJ_REPORT || {};
  (function(_) {
    if (_.BadJs) {
      return;
    }
    //onerror上报名 
    var BADJS_WIN_ERR = 'BadjsWindowError';
    var extend = function(source, destination) {
      for (var property in destination) {
        source[property] = destination[property]
      }
      return source
    }
    /*
      出错上报字段:mid name key  msg  stack file col line uin
      mid 模块名
      name 监控名
      key 特征值
      msg 额外信息
    */
    _.BadJs = {
      uin: 0,
      mid: "",
      view: "wap",
      _cache: {}, //上报_cache 同一mid name key 只会上报一次
      _info: {}, // 打点记录 会写入msg帮助定位
      _hookCallback: null,
      ignorePath: true,
      throw: function(e, extData) {
        this.onError(e, extData);
        throw e;
      },
      //接收异常并上报处理 如果有额外信息可以放在第二个参数_data中
      // _data 只能覆盖上报协议的字段mid （name,key 不建议通过data覆盖） msg  stack file col line uin
      onError: function(e, extData) {
        try {
          //标记已执行的throw
          if (e.BADJS_EXCUTED == true) {
            return;
          }
          e.BADJS_EXCUTED = true;
          var data = errToData(e);
          data.uin = this.uin;
          data.mid = this.mid;
          data.view = this.view;
          data.cmdb_module = 'mmbizwap';
          //data.msg = msg || data.msg;
          if (!!extData) {
            data = extend(data, extData);
          }
          //如果cid存在 将cid合并到key
          if (data.cid) {
            data.key = "[" + data.cid + "]:" + data.key;
          }
          
          if (data._info) {
            if (Object.prototype.toString.call(data._info) == "[object Object]") {
              data.msg += " || info:" + JSON.stringify(data._info);
            } else if (Object.prototype.toString.call(data._info) == "[object String]") {
              data.msg += " || info:" + data._info;
            } else {
              data.msg += " || info:" + data._info;
            }
          }
          if (typeof this._hookCallback == "function") {
            if (this._hookCallback(data) === false) {
              return
            }
          }
          this._send(data);
          return _.BadJs;
        } catch (e) {
          console.error(e);
        }
      },
      winErr: function(event) {
        if (event.error && event.error.BADJS_EXCUTED) {
          return;
        }
        if (event.type === 'unhandledrejection') {
          _.BadJs.onError(createError(event.type, event.reason, "", "", "", event.reason));
        }else{
          _.BadJs.onError(createError(BADJS_WIN_ERR, event.message, event.filename, event.lineno, event.colno, event.error));
        }
      },
      init: function(uin, mid, view) {
        this.uin = uin || this.uin;
        this.mid = mid || this.mid;
        this.view = view || this.view;
        return _.BadJs;
      },
      //钩子函数
      hook: function(fn) {
        this._hookCallback = fn;
        return _.BadJs;
      },
      _send: function(data) {
        //hack uin mid
        if (!data.mid) {
          if (typeof window.PAGE_MID !== 'undefined' && window.PAGE_MID) {
            data.mid = window.PAGE_MID;
          } else {
            return;
          }
        }
        if (!data.uin) {
          data.uin = window.user_uin || 0;
        }
        // 发送要去重 
        var flag = [data.mid, data.name, data.key].join("|");
        if (this._cache && this._cache[flag]) {
          return
        } else {
          this._cache && (this._cache[flag] = true);
          this._xhr(data);
        }
        return _.BadJs;
      },
      _xhr: function(data) {
        //console.log(data);
        var xmlobj;
        if (window.ActiveXObject) {
          try {
            xmlobj = new ActiveXObject("Msxml2.XMLHTTP");
          } catch (e) {
            try {
              xmlobj = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (E) {
              xmlobj = false;
            }
          }
        } else if (window.XMLHttpRequest) {
          xmlobj = new XMLHttpRequest();
        }
        var param = "";
        for (var key in data) {
          if (key && data[key]) {
            param += [key, "=", encodeURIComponent(data[key]), "&"].join("");
          }
        }
        if (xmlobj && typeof xmlobj.open == "function") {
          xmlobj.open("POST", "https://badjs.weixinbridge.com/report", true);
          xmlobj.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
          xmlobj.onreadystatechange = function(status) {};
          xmlobj.send(param.slice(0, -1));
        } else {
          var img = new Image();
          img.src = "https://badjs.weixinbridge.com/report?" + param;
        }
      },
      // key是特征值 默认上报msg就是key，也可以主动传msg包含更多上报信息 
      report: function(name, key, data) {
        this.onError(createError(name, key), data);
        return this;
      },
      // 打点标记
      mark: function(info) {
        this._info = extend(this._info, info);
      },
      nocache: function() {
        this._cache = false;
        return _.BadJs;
      }
    }
    function createError(name, msg, url, line, col, error) {
      return {
        name: name || "",
        message: msg || "",
        file: url || "",
        line: line || "",
        col: col || "",
        stack: (error && error.stack) || "",
      }
    }
    //将异常错误转换成上报协议支持的字段
    /*
    * 先取e对象上的file line col等字段
    * 再解析e.statck
    * name 错误大类 默认取badjs_try_err|badjs_win_err
    * key  错误标识 e.message
    * msg  错误信息 e.message
    * stack 错误堆栈 e.stack
    * file 错误发生的文件
    * line 行
    * col 列
    * client_version
    */
    function errToData(e) {
      var _stack = parseStack(e);
      return {
        name: e.name,
        key: e.message,
        msg: e.message,
        stack: _stack.info,
        file: _stack.file,
        line: _stack.line,
        col: _stack.col,
        client_version: "",
        _info: e._info
      }
    }
    function parseStack(e) {
      e._info = e._info || ""; // 当前错误的额外信息 最终上报到info
      var stack = e.stack || "";
      var _stack = {
        info: stack,
        file: e.file || "",
        line: e.line || "",
        col: e.col || "",
      };
      if (_stack.file == "") {
        // 提取file line col
        var stackArr = stack.split(/\bat\b/);
        if (stackArr && stackArr[1]) {
          var match = /(https?:\/\/[^\n]+)\:(\d+)\:(\d+)/.exec(stackArr[1]);
          if (match) {
            //若stack提取的file line col跟e中的属性不一致，以stack为准 但在e._info中记录原始数据
            if (match[1] && match[1] != _stack.file) {
              _stack.file && (e._info += " [file: " + _stack.file + " ]");
              _stack.file = match[1];
            }
            if (match[2] && match[2] != _stack.line) {
              _stack.line && (e._info += " [line: " + _stack.line + " ]");
              _stack.line = match[2];
            }
            if (match[3] && match[3] != _stack.col) {
              _stack.col && (e._info += " [col: " + _stack.col + " ]");
              _stack.col = match[3];
            }
          }
        }
      }
      //替换堆栈中的文件路径 combojs太长
      if (_stack && _stack.file && _stack.file.length > 0) {
        _stack.info = _stack.info.replace(new RegExp(_stack.file.split("?")[0], "gi"), "__FILE__")
      }
      //堆栈路径只保存文件名
      if (_.BadJs.ignorePath) {
        _stack.info = _stack.info.replace(/http(s)?\:[^:\n]*\//ig, "").replace(/\n/gi, "");
      }
      return _stack;
    }
    //兜底方法
    window.addEventListener && window.addEventListener('error', _.BadJs.winErr);
    window.addEventListener && window.addEventListener('unhandledrejection', _.BadJs.winErr);
    return _.BadJs;
  })(WX_BJ_REPORT);
  window.WX_BJ_REPORT = WX_BJ_REPORT;
  /**
   * 兼容wap项目的简单CMD管理
   * 所有wap项目必须包含此文件才可以执行成功
   * 暴露在全局的变量仍然以seajs为命名空间，跟web项目保持一致
   * 支持的API是seajs.use，以及require define
   * @author raphealguo
   * @date 20140326
   */
  function __moonf__() {
    if (window.__moonhasinit) return;
    window.__moonhasinit = true;
    window.__moonclientlog = []; // moon中存到客户端日志里面的内容，最终写入到客户端的地点在fereport.js
    if (typeof JSON != "object") { //针对IE7的hack
      window.JSON = {
        stringify: function() { return ""; },
        parse: function() { return {}; }
      };
    }
    var moon_init = function() {
      /**
       * mooncatch
       * 对各种异步回调都使用try catch错误上报
       * @radeonwu raphealguo
       */
      (function() {
        var inWx = (/MicroMessenger/i).test(navigator.userAgent);
        var inMp = (/MPAPP/i).test(navigator.userAgent);
        var _idkey = 121261; //上报的idkey 添加默认上报值
        var _startKey; //开始的key
        var _limit; //上报的key的长度
        var _badjsId;
        var _reportOpt; //上报的额外信息
        var _extInfo; //附加的预留字段，如网络采样率采样率network_rate， 总体上报率rate
        var MOON_AJAX_NETWORK_OFFSET = 4; //network错误时的上报偏移量为4，这里在ajax.js中上报，这里需要加入采样率
        window.__initCatch = function(opt) {
          _idkey = opt.idkey;
          _startKey = opt.startKey || 0;
          _limit = opt.limit;
          _badjsId = opt.badjsId;
          _reportOpt = opt.reportOpt || "";
          _extInfo = opt.extInfo || {};
          _extInfo.rate = _extInfo.rate || 0.5;
        }
        //暴露的上报函数，供core.js和ajax.js上报错误使用，array = [{offset:MOON_JSAPI_KEY_OFFSET, log:"ready", e:e}]
        window.__moon_report = function(array, rate_opt) {
          var isAcrossOrigin = false;
          var href = '';
          try {
            href = top.location.href;
          } catch (e) {
            isAcrossOrigin = true;
          }
          var rate = 0.5;
          if (!!_extInfo && !!_extInfo.rate) {
            rate = _extInfo.rate;
          }
          if (!!rate_opt && (typeof rate_opt == 'number')) {
            rate = rate_opt;
          }
          if (
            (!(/mp\.weixin\.qq\.com/).test(location.href) && !(/payapp\.weixin\.qq\.com/).test(location.href)) ||
            Math.random() > rate ||
            !(inWx || inMp) ||
            (top != window && !isAcrossOrigin && !(/mp\.weixin\.qq\.com/).test(href))
          ) {
            //return ;
          }
          if (isObject(array))
            array = [array];
          if (!isArray(array) || _idkey == '')
            return;
          var data = "";
          var log = []; //存放array中每个对象关联的log
          var key = []; //存放array中每个上报的key
          var val = []; //存放array中每个上报的value
          var idkey = [];
          //如果这里没有opt.limit，直接上报到startKey
          if (typeof _limit != "number") {
            _limit = Infinity;
          }
          for (var i = 0; i < array.length; i++) {
            var item = array[i] || {};
            if (item.offset > _limit) continue; //上报的偏移量超过limit
            if (typeof item.offset != "number") continue;
            if (item.offset == MOON_AJAX_NETWORK_OFFSET && !!_extInfo && !!_extInfo.network_rate && Math.random() >= _extInfo.network_rate) {
              continue;
            }
            //log[i] = item.log || "";
            var k = _limit == Infinity ? _startKey : (_startKey + item.offset);
            log[i] = (("[moon]" + _idkey + "_" + k + ";") + item.log + ";" + getErrorMessage(item.e || {})) || "";
            key[i] = k;
            val[i] = 1;
          }
          for (var j = 0; j < key.length; j++) {
            idkey[j] = _idkey + "_" + key[j] + "_" + val[j];
            data = data + "&log" + j + "=" + log[j];
          }
          if (idkey.length > 0) {
            // sendReport("idkey=" + idkey.join(";") + "&lc=" + log.length + data);
            sendReport("POST", location.protocol + '//mp.weixin.qq.com/mp/jsmonitor?', "idkey=" + idkey.join(";") + "&r=" + Math.random() + "&lc=" + log.length + data);
            // 把图文消息的错误上报一份到badjs，只支持get请求
            // 这里由于量比较大，把badjs的内层怼爆了，这里加多一个采样，并且去掉用户的信息
            var rate = 1;
            if (_extInfo && _extInfo.badjs_rate) { // 初始化时的badjs采样率
              rate = _extInfo.badjs_rate;
            }
            if (Math.random() < rate) {
              data = data.replace(/uin\:(.)*\|biz\:(.)*\|mid\:(.)*\|idx\:(.)*\|sn\:(.)*\|/, '');
              if(!!_badjsId){
                var _img = new Image();
                var _src = 'https://badjs.weixinbridge.com/badjs?id=' + _badjsId + '&level=4&from=' + encodeURIComponent(location.host) + '&msg=' + encodeURIComponent(data);
                _img.src = _src.slice(0, 1024);
              }
              // badjs同时报一份到新监控 
              if (typeof WX_BJ_REPORT != "undefined" && WX_BJ_REPORT.BadJs) {
                for (var i = 0; i < array.length; i++) {
                  var item = array[i] || {};
                  if (item.e) {
                    WX_BJ_REPORT.BadJs.onError(item.e,{_info:item.log});
                  } else {
                    var name = /[^:;]*/.exec(item.log)[0];
                    WX_BJ_REPORT.BadJs.report(name, item.log, { mid: "mmbizwap:Monitor" });
                  }
                }
              }
            } else {
              //虽然采样没有执行 但实际是有被BadJs.onError，置位一下
              for (var i = 0; i < array.length; i++) {
                var item = array[i] || {};
                if (item.e) {
                  item.e.BADJS_EXCUTED = true;
                }
              }
            }
          }
        }
        function isArray(obj) { //判断输入是否为数组
          return Object.prototype.toString.call(obj) === '[object Array]';
        }
        function isObject(obj) { //判断输入是否为对象
          return Object.prototype.toString.call(obj) === '[object Object]';
        }
        function getErrorMessage(e) {
          var stack = e.stack + ' ' + e.toString() || ""; //错误堆栈信息
          try {
            //先取出res域名
            if (!window.testenv_reshost) {
              stack = stack.replace(/http(s)?:\/\/res\.wx\.qq\.com/g, "");
            } else {
              var host = 'http(s)?://' + window.testenv_reshost;
              var reg = new RegExp(host, 'g');
              stack = stack.replace(reg, "");
            }
            //提取最后一个.js前边的
            var reg = /\/([^.]+)\/js\/(\S+?)\.js(\,|:)?/g;
            while (reg.test(stack)) {
              // stack = stack.replace(reg, "3"); 解决$问题
              stack = stack.replace(reg, function(a, b, c, d, e, f) {
                return c + d
              });
            }
          } catch (e) {
            stack = e.stack ? e.stack : "" //错误堆栈信息
          }
          var ret = [];
          for (o in _reportOpt) {
            if (_reportOpt.hasOwnProperty(o)) {
              ret.push(o + ":" + _reportOpt[o]);
            }
          }
          ret.push("STK:" + stack.replace(/\n/g, ""));
          return ret.join("|");
        }
        function sendReport(type, url, data) { //post方法用于提交数据
          if (!/^mp\.weixin\.qq\.com$/.test(location.hostname)) { //非MP域名使用 img方式上报
            var tmp = [];
            data = data.replace(location.href, (location.origin || "") + (location.pathname || "")).replace("#wechat_redirect", "").replace("#rd", "").split("&");
            for (var i = 0, il = data.length; i < il; i++) {
              var a = data[i].split("=");
              if (!!a[0] && !!a[1]) {
                tmp.push(a[0] + "=" + encodeURIComponent(a[1]));
              }
            }
            var _img = new window.Image();
            _img.src = (url + tmp.join("&")).substr(0, 1024);
            return;
          }
          var xmlobj; //定义XMLHttpRequest对象  
          if (window.ActiveXObject) { //如果当前浏览器支持Active Xobject，则创建ActiveXObject对象    
            try {
              xmlobj = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
              try {
                xmlobj = new ActiveXObject("Microsoft.XMLHTTP");
              } catch (E) {
                xmlobj = false;
              }
            }
          } else if (window.XMLHttpRequest) { //如果当前浏览器支持XMLHttpRequest，则创建XMLHttpRequest对象  
            xmlobj = new XMLHttpRequest();
          }
          if (!xmlobj) return;
          //xmlobj.open("POST", location.protocol + "//mp.weixin.qq.com/mp/jsmonitor?", true);         
          xmlobj.open(type, url, true);
          xmlobj.setRequestHeader("cache-control", "no-cache");
          xmlobj.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"); //设置请求头信息              
          xmlobj.setRequestHeader("X-Requested-With", "XMLHttpRequest");
          xmlobj.send(data); //发送数据  
        }

      })();
      // 后面的@cunjinli
    };
    moon_init();
    //由于moon异步化，所以有些逻辑需要moon加载完之后才执行的 放到全局callback函数__moon_initcallback里边
    (!!window.__moon_initcallback) && (window.__moon_initcallback());
  }
  // 为适应inline逻辑，有map时才主动自执行 @zhikaimai
  // if (typeof window.moon_map == 'object') {
  //     __moonf__();
  // }
  __moonf__();
  
  if (!!window.addEventListener){
    window.addEventListener("load",function(){
      var MOON_SCRIPT_ERROR_KEY_OFFSET = 1; //script上报时的偏移量为1
      var ns = document.querySelectorAll("[reportloaderror]");
      for(var ni=0,nl=ns.length;ni<nl;ni++)
        ns[ni].onerror=function(ev){
          window.__moon_report([{ offset: MOON_SCRIPT_ERROR_KEY_OFFSET, log: "load_script_error:" + ev.target.src, e: new Error('LoadResError') }], 1);
          window.WX_BJ_REPORT.BadJs.report("load_script_error", ev.target.src, { mid: "mmbizwap:Monitor" });
        };
    });
  }
  </script>
   
    

  
  <meta name="description" content="楔子这一次我们分析一下Python的字符串，首先字符串是一个变长对象，因为不同长度的字符串所占的内存是不一样" />
  <meta name="author" content="古明地觉" />

  
  <meta property="og:title" content="《源码探秘 CPython》19. 字符集和字符编码" />
  <meta property="og:url" content="http://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&amp;mid=2247483828&amp;idx=1&amp;sn=41345986a28feb40bb7e80b985300b6f&amp;chksm=cf3c4259f84bcb4fa1fc9887b41b1a230980dea2a1027206e11641d4c0e3506b92464bc2b51c#rd" />
  <meta property="og:image" content="http://mmbiz.qpic.cn/sz_mmbiz_jpg/ib8ibwulXslsHPAO4fnichyQJPcF7VVYQv82UYZm0HeSUicM0ibImRjibSicRvvTpAkBlRsEaAz2LujORrwF6JqeticYSQ/0?wx_fmt=jpeg" />
  <meta property="og:description" content="楔子这一次我们分析一下Python的字符串，首先字符串是一个变长对象，因为不同长度的字符串所占的内存是不一样" />
  <meta property="og:site_name" content="微信公众平台" />
  <meta property="og:type" content="article" />
  <meta property="og:article:author" content="古明地觉" />

  
  <meta property="twitter:card" content="summary" />
  <meta property="twitter:image" content="http://mmbiz.qpic.cn/sz_mmbiz_jpg/ib8ibwulXslsHPAO4fnichyQJPcF7VVYQv82UYZm0HeSUicM0ibImRjibSicRvvTpAkBlRsEaAz2LujORrwF6JqeticYSQ/0?wx_fmt=jpeg" />
  <meta property="twitter:title" content="《源码探秘 CPython》19. 字符集和字符编码" />
  <meta property="twitter:creator" content="古明地觉" />
  <meta property="twitter:site" content="微信公众平台" />
  <meta property="twitter:description" content="楔子这一次我们分析一下Python的字符串，首先字符串是一个变长对象，因为不同长度的字符串所占的内存是不一样" />


    <title></title>
    <script  nonce="1682091926" reportloaderror>
    (() => {
      // 初始 title 为空时，给 pc 端设置默认 title @bolewang
      const ua = navigator.userAgent;
      const noMobile = !(/(iPhone|iPad|iPod|iOS)/i.test(ua) || /Windows\sPhone/i.test(ua) || /(Android)/i.test(ua));
      setTimeout(() => {
        noMobile && document.title === '' && (document.title = '微信公众平台');
      }, 1000);
    })();
    </script>
    

<script h5only type="text/javascript" nonce="1682091926" reportloaderror>/*!
 * Vue.js v2.6.14
 * (c) 2014-2021 Evan You
 * Released under the MIT License.
 */
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(t=t||self).Vue=e()}(this,function(){"use strict";var t=Object.freeze({});function e(t){return null==t}function n(t){return null!=t}function r(t){return!0===t}function o(t){return"string"==typeof t||"number"==typeof t||"symbol"==typeof t||"boolean"==typeof t}function i(t){return null!==t&&"object"==typeof t}var a=Object.prototype.toString;function s(t){return"[object Object]"===a.call(t)}function c(t){var e=parseFloat(String(t));return e>=0&&Math.floor(e)===e&&isFinite(t)}function u(t){return n(t)&&"function"==typeof t.then&&"function"==typeof t.catch}function l(t){return null==t?"":Array.isArray(t)||s(t)&&t.toString===a?JSON.stringify(t,null,2):String(t)}function f(t){var e=parseFloat(t);return isNaN(e)?t:e}function d(t,e){for(var n=Object.create(null),r=t.split(","),o=0;o<r.length;o++)n[r[o]]=!0;return e?function(t){return n[t.toLowerCase()]}:function(t){return n[t]}}var p=d("key,ref,slot,slot-scope,is");function v(t,e){if(t.length){var n=t.indexOf(e);if(n>-1)return t.splice(n,1)}}var h=Object.prototype.hasOwnProperty;function m(t,e){return h.call(t,e)}function y(t){var e=Object.create(null);return function(n){return e[n]||(e[n]=t(n))}}var g=/-(\w)/g,_=y(function(t){return t.replace(g,function(t,e){return e?e.toUpperCase():""})}),b=y(function(t){return t.charAt(0).toUpperCase()+t.slice(1)}),C=/\B([A-Z])/g,$=y(function(t){return t.replace(C,"-$1").toLowerCase()});var w=Function.prototype.bind?function(t,e){return t.bind(e)}:function(t,e){function n(n){var r=arguments.length;return r?r>1?t.apply(e,arguments):t.call(e,n):t.call(e)}return n._length=t.length,n};function A(t,e){e=e||0;for(var n=t.length-e,r=new Array(n);n--;)r[n]=t[n+e];return r}function x(t,e){for(var n in e)t[n]=e[n];return t}function k(t){for(var e={},n=0;n<t.length;n++)t[n]&&x(e,t[n]);return e}function O(t,e,n){}var S=function(t,e,n){return!1},E=function(t){return t};function T(t,e){if(t===e)return!0;var n=i(t),r=i(e);if(!n||!r)return!n&&!r&&String(t)===String(e);try{var o=Array.isArray(t),a=Array.isArray(e);if(o&&a)return t.length===e.length&&t.every(function(t,n){return T(t,e[n])});if(t instanceof Date&&e instanceof Date)return t.getTime()===e.getTime();if(o||a)return!1;var s=Object.keys(t),c=Object.keys(e);return s.length===c.length&&s.every(function(n){return T(t[n],e[n])})}catch(t){return!1}}function j(t,e){for(var n=0;n<t.length;n++)if(T(t[n],e))return n;return-1}function I(t){var e=!1;return function(){e||(e=!0,t.apply(this,arguments))}}var D="data-server-rendered",N=["component","directive","filter"],P=["beforeCreate","created","beforeMount","mounted","beforeUpdate","updated","beforeDestroy","destroyed","activated","deactivated","errorCaptured","serverPrefetch"],L={optionMergeStrategies:Object.create(null),silent:!1,productionTip:!1,devtools:!1,performance:!1,errorHandler:null,warnHandler:null,ignoredElements:[],keyCodes:Object.create(null),isReservedTag:S,isReservedAttr:S,isUnknownElement:S,getTagNamespace:O,parsePlatformTagName:E,mustUseProp:S,async:!0,_lifecycleHooks:P};function M(t,e,n,r){Object.defineProperty(t,e,{value:n,enumerable:!!r,writable:!0,configurable:!0})}var F=new RegExp("[^"+/a-zA-Z\u00B7\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u037D\u037F-\u1FFF\u200C-\u200D\u203F-\u2040\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD/.source+".$_\\d]");var R,V="__proto__"in{},U="undefined"!=typeof window,H="undefined"!=typeof WXEnvironment&&!!WXEnvironment.platform,B=H&&WXEnvironment.platform.toLowerCase(),z=U&&window.navigator.userAgent.toLowerCase(),W=z&&/msie|trident/.test(z),q=z&&z.indexOf("msie 9.0")>0,K=z&&z.indexOf("edge/")>0,X=(z&&z.indexOf("android"),z&&/iphone|ipad|ipod|ios/.test(z)||"ios"===B),G=(z&&/chrome\/\d+/.test(z),z&&/phantomjs/.test(z),z&&z.match(/firefox\/(\d+)/)),Z={}.watch,J=!1;if(U)try{var Q={};Object.defineProperty(Q,"passive",{get:function(){J=!0}}),window.addEventListener("test-passive",null,Q)}catch(t){}var Y=function(){return void 0===R&&(R=!U&&!H&&"undefined"!=typeof global&&(global.process&&"server"===global.process.env.VUE_ENV)),R},tt=U&&window.__VUE_DEVTOOLS_GLOBAL_HOOK__;function et(t){return"function"==typeof t&&/native code/.test(t.toString())}var nt,rt="undefined"!=typeof Symbol&&et(Symbol)&&"undefined"!=typeof Reflect&&et(Reflect.ownKeys);nt="undefined"!=typeof Set&&et(Set)?Set:function(){function t(){this.set=Object.create(null)}return t.prototype.has=function(t){return!0===this.set[t]},t.prototype.add=function(t){this.set[t]=!0},t.prototype.clear=function(){this.set=Object.create(null)},t}();var ot=O,it=0,at=function(){this.id=it++,this.subs=[]};at.prototype.addSub=function(t){this.subs.push(t)},at.prototype.removeSub=function(t){v(this.subs,t)},at.prototype.depend=function(){at.target&&at.target.addDep(this)},at.prototype.notify=function(){for(var t=this.subs.slice(),e=0,n=t.length;e<n;e++)t[e].update()},at.target=null;var st=[];function ct(t){st.push(t),at.target=t}function ut(){st.pop(),at.target=st[st.length-1]}var lt=function(t,e,n,r,o,i,a,s){this.tag=t,this.data=e,this.children=n,this.text=r,this.elm=o,this.ns=void 0,this.context=i,this.fnContext=void 0,this.fnOptions=void 0,this.fnScopeId=void 0,this.key=e&&e.key,this.componentOptions=a,this.componentInstance=void 0,this.parent=void 0,this.raw=!1,this.isStatic=!1,this.isRootInsert=!0,this.isComment=!1,this.isCloned=!1,this.isOnce=!1,this.asyncFactory=s,this.asyncMeta=void 0,this.isAsyncPlaceholder=!1},ft={child:{configurable:!0}};ft.child.get=function(){return this.componentInstance},Object.defineProperties(lt.prototype,ft);var dt=function(t){void 0===t&&(t="");var e=new lt;return e.text=t,e.isComment=!0,e};function pt(t){return new lt(void 0,void 0,void 0,String(t))}function vt(t){var e=new lt(t.tag,t.data,t.children&&t.children.slice(),t.text,t.elm,t.context,t.componentOptions,t.asyncFactory);return e.ns=t.ns,e.isStatic=t.isStatic,e.key=t.key,e.isComment=t.isComment,e.fnContext=t.fnContext,e.fnOptions=t.fnOptions,e.fnScopeId=t.fnScopeId,e.asyncMeta=t.asyncMeta,e.isCloned=!0,e}var ht=Array.prototype,mt=Object.create(ht);["push","pop","shift","unshift","splice","sort","reverse"].forEach(function(t){var e=ht[t];M(mt,t,function(){for(var n=[],r=arguments.length;r--;)n[r]=arguments[r];var o,i=e.apply(this,n),a=this.__ob__;switch(t){case"push":case"unshift":o=n;break;case"splice":o=n.slice(2)}return o&&a.observeArray(o),a.dep.notify(),i})});var yt=Object.getOwnPropertyNames(mt),gt=!0;function _t(t){gt=t}var bt=function(t){var e;this.value=t,this.dep=new at,this.vmCount=0,M(t,"__ob__",this),Array.isArray(t)?(V?(e=mt,t.__proto__=e):function(t,e,n){for(var r=0,o=n.length;r<o;r++){var i=n[r];M(t,i,e[i])}}(t,mt,yt),this.observeArray(t)):this.walk(t)};function Ct(t,e){var n;if(i(t)&&!(t instanceof lt))return m(t,"__ob__")&&t.__ob__ instanceof bt?n=t.__ob__:gt&&!Y()&&(Array.isArray(t)||s(t))&&Object.isExtensible(t)&&!t._isVue&&(n=new bt(t)),e&&n&&n.vmCount++,n}function $t(t,e,n,r,o){var i=new at,a=Object.getOwnPropertyDescriptor(t,e);if(!a||!1!==a.configurable){var s=a&&a.get,c=a&&a.set;s&&!c||2!==arguments.length||(n=t[e]);var u=!o&&Ct(n);Object.defineProperty(t,e,{enumerable:!0,configurable:!0,get:function(){var e=s?s.call(t):n;return at.target&&(i.depend(),u&&(u.dep.depend(),Array.isArray(e)&&function t(e){for(var n=void 0,r=0,o=e.length;r<o;r++)(n=e[r])&&n.__ob__&&n.__ob__.dep.depend(),Array.isArray(n)&&t(n)}(e))),e},set:function(e){var r=s?s.call(t):n;e===r||e!=e&&r!=r||s&&!c||(c?c.call(t,e):n=e,u=!o&&Ct(e),i.notify())}})}}function wt(t,e,n){if(Array.isArray(t)&&c(e))return t.length=Math.max(t.length,e),t.splice(e,1,n),n;if(e in t&&!(e in Object.prototype))return t[e]=n,n;var r=t.__ob__;return t._isVue||r&&r.vmCount?n:r?($t(r.value,e,n),r.dep.notify(),n):(t[e]=n,n)}function At(t,e){if(Array.isArray(t)&&c(e))t.splice(e,1);else{var n=t.__ob__;t._isVue||n&&n.vmCount||m(t,e)&&(delete t[e],n&&n.dep.notify())}}bt.prototype.walk=function(t){for(var e=Object.keys(t),n=0;n<e.length;n++)$t(t,e[n])},bt.prototype.observeArray=function(t){for(var e=0,n=t.length;e<n;e++)Ct(t[e])};var xt=L.optionMergeStrategies;function kt(t,e){if(!e)return t;for(var n,r,o,i=rt?Reflect.ownKeys(e):Object.keys(e),a=0;a<i.length;a++)"__ob__"!==(n=i[a])&&(r=t[n],o=e[n],m(t,n)?r!==o&&s(r)&&s(o)&&kt(r,o):wt(t,n,o));return t}function Ot(t,e,n){return n?function(){var r="function"==typeof e?e.call(n,n):e,o="function"==typeof t?t.call(n,n):t;return r?kt(r,o):o}:e?t?function(){return kt("function"==typeof e?e.call(this,this):e,"function"==typeof t?t.call(this,this):t)}:e:t}function St(t,e){var n=e?t?t.concat(e):Array.isArray(e)?e:[e]:t;return n?function(t){for(var e=[],n=0;n<t.length;n++)-1===e.indexOf(t[n])&&e.push(t[n]);return e}(n):n}function Et(t,e,n,r){var o=Object.create(t||null);return e?x(o,e):o}xt.data=function(t,e,n){return n?Ot(t,e,n):e&&"function"!=typeof e?t:Ot(t,e)},P.forEach(function(t){xt[t]=St}),N.forEach(function(t){xt[t+"s"]=Et}),xt.watch=function(t,e,n,r){if(t===Z&&(t=void 0),e===Z&&(e=void 0),!e)return Object.create(t||null);if(!t)return e;var o={};for(var i in x(o,t),e){var a=o[i],s=e[i];a&&!Array.isArray(a)&&(a=[a]),o[i]=a?a.concat(s):Array.isArray(s)?s:[s]}return o},xt.props=xt.methods=xt.inject=xt.computed=function(t,e,n,r){if(!t)return e;var o=Object.create(null);return x(o,t),e&&x(o,e),o},xt.provide=Ot;var Tt=function(t,e){return void 0===e?t:e};function jt(t,e,n){if("function"==typeof e&&(e=e.options),function(t,e){var n=t.props;if(n){var r,o,i={};if(Array.isArray(n))for(r=n.length;r--;)"string"==typeof(o=n[r])&&(i[_(o)]={type:null});else if(s(n))for(var a in n)o=n[a],i[_(a)]=s(o)?o:{type:o};t.props=i}}(e),function(t,e){var n=t.inject;if(n){var r=t.inject={};if(Array.isArray(n))for(var o=0;o<n.length;o++)r[n[o]]={from:n[o]};else if(s(n))for(var i in n){var a=n[i];r[i]=s(a)?x({from:i},a):{from:a}}}}(e),function(t){var e=t.directives;if(e)for(var n in e){var r=e[n];"function"==typeof r&&(e[n]={bind:r,update:r})}}(e),!e._base&&(e.extends&&(t=jt(t,e.extends,n)),e.mixins))for(var r=0,o=e.mixins.length;r<o;r++)t=jt(t,e.mixins[r],n);var i,a={};for(i in t)c(i);for(i in e)m(t,i)||c(i);function c(r){var o=xt[r]||Tt;a[r]=o(t[r],e[r],n,r)}return a}function It(t,e,n,r){if("string"==typeof n){var o=t[e];if(m(o,n))return o[n];var i=_(n);if(m(o,i))return o[i];var a=b(i);return m(o,a)?o[a]:o[n]||o[i]||o[a]}}function Dt(t,e,n,r){var o=e[t],i=!m(n,t),a=n[t],s=Mt(Boolean,o.type);if(s>-1)if(i&&!m(o,"default"))a=!1;else if(""===a||a===$(t)){var c=Mt(String,o.type);(c<0||s<c)&&(a=!0)}if(void 0===a){a=function(t,e,n){if(!m(e,"default"))return;var r=e.default;if(t&&t.$options.propsData&&void 0===t.$options.propsData[n]&&void 0!==t._props[n])return t._props[n];return"function"==typeof r&&"Function"!==Pt(e.type)?r.call(t):r}(r,o,t);var u=gt;_t(!0),Ct(a),_t(u)}return a}var Nt=/^\s*function (\w+)/;function Pt(t){var e=t&&t.toString().match(Nt);return e?e[1]:""}function Lt(t,e){return Pt(t)===Pt(e)}function Mt(t,e){if(!Array.isArray(e))return Lt(e,t)?0:-1;for(var n=0,r=e.length;n<r;n++)if(Lt(e[n],t))return n;return-1}function Ft(t,e,n){ct();try{if(e)for(var r=e;r=r.$parent;){var o=r.$options.errorCaptured;if(o)for(var i=0;i<o.length;i++)try{if(!1===o[i].call(r,t,e,n))return}catch(t){Vt(t,r,"errorCaptured hook")}}Vt(t,e,n)}finally{ut()}}function Rt(t,e,n,r,o){var i;try{(i=n?t.apply(e,n):t.call(e))&&!i._isVue&&u(i)&&!i._handled&&(i.catch(function(t){return Ft(t,r,o+" (Promise/async)")}),i._handled=!0)}catch(t){Ft(t,r,o)}return i}function Vt(t,e,n){if(L.errorHandler)try{return L.errorHandler.call(null,t,e,n)}catch(e){e!==t&&Ut(e,null,"config.errorHandler")}Ut(t,e,n)}function Ut(t,e,n){if(!U&&!H||"undefined"==typeof console)throw t;console.error(t)}var Ht,Bt=!1,zt=[],Wt=!1;function qt(){Wt=!1;var t=zt.slice(0);zt.length=0;for(var e=0;e<t.length;e++)t[e]()}if("undefined"!=typeof Promise&&et(Promise)){var Kt=Promise.resolve();Ht=function(){Kt.then(qt),X&&setTimeout(O)},Bt=!0}else if(W||"undefined"==typeof MutationObserver||!et(MutationObserver)&&"[object MutationObserverConstructor]"!==MutationObserver.toString())Ht="undefined"!=typeof setImmediate&&et(setImmediate)?function(){setImmediate(qt)}:function(){setTimeout(qt,0)};else{var Xt=1,Gt=new MutationObserver(qt),Zt=document.createTextNode(String(Xt));Gt.observe(Zt,{characterData:!0}),Ht=function(){Xt=(Xt+1)%2,Zt.data=String(Xt)},Bt=!0}function Jt(t,e){var n;if(zt.push(function(){if(t)try{t.call(e)}catch(t){Ft(t,e,"nextTick")}else n&&n(e)}),Wt||(Wt=!0,Ht()),!t&&"undefined"!=typeof Promise)return new Promise(function(t){n=t})}var Qt=new nt;function Yt(t){!function t(e,n){var r,o;var a=Array.isArray(e);if(!a&&!i(e)||Object.isFrozen(e)||e instanceof lt)return;if(e.__ob__){var s=e.__ob__.dep.id;if(n.has(s))return;n.add(s)}if(a)for(r=e.length;r--;)t(e[r],n);else for(o=Object.keys(e),r=o.length;r--;)t(e[o[r]],n)}(t,Qt),Qt.clear()}var te=y(function(t){var e="&"===t.charAt(0),n="~"===(t=e?t.slice(1):t).charAt(0),r="!"===(t=n?t.slice(1):t).charAt(0);return{name:t=r?t.slice(1):t,once:n,capture:r,passive:e}});function ee(t,e){function n(){var t=arguments,r=n.fns;if(!Array.isArray(r))return Rt(r,null,arguments,e,"v-on handler");for(var o=r.slice(),i=0;i<o.length;i++)Rt(o[i],null,t,e,"v-on handler")}return n.fns=t,n}function ne(t,n,o,i,a,s){var c,u,l,f;for(c in t)u=t[c],l=n[c],f=te(c),e(u)||(e(l)?(e(u.fns)&&(u=t[c]=ee(u,s)),r(f.once)&&(u=t[c]=a(f.name,u,f.capture)),o(f.name,u,f.capture,f.passive,f.params)):u!==l&&(l.fns=u,t[c]=l));for(c in n)e(t[c])&&i((f=te(c)).name,n[c],f.capture)}function re(t,o,i){var a;t instanceof lt&&(t=t.data.hook||(t.data.hook={}));var s=t[o];function c(){i.apply(this,arguments),v(a.fns,c)}e(s)?a=ee([c]):n(s.fns)&&r(s.merged)?(a=s).fns.push(c):a=ee([s,c]),a.merged=!0,t[o]=a}function oe(t,e,r,o,i){if(n(e)){if(m(e,r))return t[r]=e[r],i||delete e[r],!0;if(m(e,o))return t[r]=e[o],i||delete e[o],!0}return!1}function ie(t){return o(t)?[pt(t)]:Array.isArray(t)?function t(i,a){var s=[];var c,u,l,f;for(c=0;c<i.length;c++)e(u=i[c])||"boolean"==typeof u||(l=s.length-1,f=s[l],Array.isArray(u)?u.length>0&&(ae((u=t(u,(a||"")+"_"+c))[0])&&ae(f)&&(s[l]=pt(f.text+u[0].text),u.shift()),s.push.apply(s,u)):o(u)?ae(f)?s[l]=pt(f.text+u):""!==u&&s.push(pt(u)):ae(u)&&ae(f)?s[l]=pt(f.text+u.text):(r(i._isVList)&&n(u.tag)&&e(u.key)&&n(a)&&(u.key="__vlist"+a+"_"+c+"__"),s.push(u)));return s}(t):void 0}function ae(t){return n(t)&&n(t.text)&&!1===t.isComment}function se(t,e){if(t){for(var n=Object.create(null),r=rt?Reflect.ownKeys(t):Object.keys(t),o=0;o<r.length;o++){var i=r[o];if("__ob__"!==i){for(var a=t[i].from,s=e;s;){if(s._provided&&m(s._provided,a)){n[i]=s._provided[a];break}s=s.$parent}if(!s&&"default"in t[i]){var c=t[i].default;n[i]="function"==typeof c?c.call(e):c}}}return n}}function ce(t,e){if(!t||!t.length)return{};for(var n={},r=0,o=t.length;r<o;r++){var i=t[r],a=i.data;if(a&&a.attrs&&a.attrs.slot&&delete a.attrs.slot,i.context!==e&&i.fnContext!==e||!a||null==a.slot)(n.default||(n.default=[])).push(i);else{var s=a.slot,c=n[s]||(n[s]=[]);"template"===i.tag?c.push.apply(c,i.children||[]):c.push(i)}}for(var u in n)n[u].every(ue)&&delete n[u];return n}function ue(t){return t.isComment&&!t.asyncFactory||" "===t.text}function le(t){return t.isComment&&t.asyncFactory}function fe(e,n,r){var o,i=Object.keys(n).length>0,a=e?!!e.$stable:!i,s=e&&e.$key;if(e){if(e._normalized)return e._normalized;if(a&&r&&r!==t&&s===r.$key&&!i&&!r.$hasNormal)return r;for(var c in o={},e)e[c]&&"$"!==c[0]&&(o[c]=de(n,c,e[c]))}else o={};for(var u in n)u in o||(o[u]=pe(n,u));return e&&Object.isExtensible(e)&&(e._normalized=o),M(o,"$stable",a),M(o,"$key",s),M(o,"$hasNormal",i),o}function de(t,e,n){var r=function(){var t=arguments.length?n.apply(null,arguments):n({}),e=(t=t&&"object"==typeof t&&!Array.isArray(t)?[t]:ie(t))&&t[0];return t&&(!e||1===t.length&&e.isComment&&!le(e))?void 0:t};return n.proxy&&Object.defineProperty(t,e,{get:r,enumerable:!0,configurable:!0}),r}function pe(t,e){return function(){return t[e]}}function ve(t,e){var r,o,a,s,c;if(Array.isArray(t)||"string"==typeof t)for(r=new Array(t.length),o=0,a=t.length;o<a;o++)r[o]=e(t[o],o);else if("number"==typeof t)for(r=new Array(t),o=0;o<t;o++)r[o]=e(o+1,o);else if(i(t))if(rt&&t[Symbol.iterator]){r=[];for(var u=t[Symbol.iterator](),l=u.next();!l.done;)r.push(e(l.value,r.length)),l=u.next()}else for(s=Object.keys(t),r=new Array(s.length),o=0,a=s.length;o<a;o++)c=s[o],r[o]=e(t[c],c,o);return n(r)||(r=[]),r._isVList=!0,r}function he(t,e,n,r){var o,i=this.$scopedSlots[t];i?(n=n||{},r&&(n=x(x({},r),n)),o=i(n)||("function"==typeof e?e():e)):o=this.$slots[t]||("function"==typeof e?e():e);var a=n&&n.slot;return a?this.$createElement("template",{slot:a},o):o}function me(t){return It(this.$options,"filters",t)||E}function ye(t,e){return Array.isArray(t)?-1===t.indexOf(e):t!==e}function ge(t,e,n,r,o){var i=L.keyCodes[e]||n;return o&&r&&!L.keyCodes[e]?ye(o,r):i?ye(i,t):r?$(r)!==e:void 0===t}function _e(t,e,n,r,o){if(n)if(i(n)){var a;Array.isArray(n)&&(n=k(n));var s=function(i){if("class"===i||"style"===i||p(i))a=t;else{var s=t.attrs&&t.attrs.type;a=r||L.mustUseProp(e,s,i)?t.domProps||(t.domProps={}):t.attrs||(t.attrs={})}var c=_(i),u=$(i);c in a||u in a||(a[i]=n[i],o&&((t.on||(t.on={}))["update:"+i]=function(t){n[i]=t}))};for(var c in n)s(c)}else;return t}function be(t,e){var n=this._staticTrees||(this._staticTrees=[]),r=n[t];return r&&!e?r:($e(r=n[t]=this.$options.staticRenderFns[t].call(this._renderProxy,null,this),"__static__"+t,!1),r)}function Ce(t,e,n){return $e(t,"__once__"+e+(n?"_"+n:""),!0),t}function $e(t,e,n){if(Array.isArray(t))for(var r=0;r<t.length;r++)t[r]&&"string"!=typeof t[r]&&we(t[r],e+"_"+r,n);else we(t,e,n)}function we(t,e,n){t.isStatic=!0,t.key=e,t.isOnce=n}function Ae(t,e){if(e)if(s(e)){var n=t.on=t.on?x({},t.on):{};for(var r in e){var o=n[r],i=e[r];n[r]=o?[].concat(o,i):i}}else;return t}function xe(t,e,n,r){e=e||{$stable:!n};for(var o=0;o<t.length;o++){var i=t[o];Array.isArray(i)?xe(i,e,n):i&&(i.proxy&&(i.fn.proxy=!0),e[i.key]=i.fn)}return r&&(e.$key=r),e}function ke(t,e){for(var n=0;n<e.length;n+=2){var r=e[n];"string"==typeof r&&r&&(t[e[n]]=e[n+1])}return t}function Oe(t,e){return"string"==typeof t?e+t:t}function Se(t){t._o=Ce,t._n=f,t._s=l,t._l=ve,t._t=he,t._q=T,t._i=j,t._m=be,t._f=me,t._k=ge,t._b=_e,t._v=pt,t._e=dt,t._u=xe,t._g=Ae,t._d=ke,t._p=Oe}function Ee(e,n,o,i,a){var s,c=this,u=a.options;m(i,"_uid")?(s=Object.create(i))._original=i:(s=i,i=i._original);var l=r(u._compiled),f=!l;this.data=e,this.props=n,this.children=o,this.parent=i,this.listeners=e.on||t,this.injections=se(u.inject,i),this.slots=function(){return c.$slots||fe(e.scopedSlots,c.$slots=ce(o,i)),c.$slots},Object.defineProperty(this,"scopedSlots",{enumerable:!0,get:function(){return fe(e.scopedSlots,this.slots())}}),l&&(this.$options=u,this.$slots=this.slots(),this.$scopedSlots=fe(e.scopedSlots,this.$slots)),u._scopeId?this._c=function(t,e,n,r){var o=Fe(s,t,e,n,r,f);return o&&!Array.isArray(o)&&(o.fnScopeId=u._scopeId,o.fnContext=i),o}:this._c=function(t,e,n,r){return Fe(s,t,e,n,r,f)}}function Te(t,e,n,r,o){var i=vt(t);return i.fnContext=n,i.fnOptions=r,e.slot&&((i.data||(i.data={})).slot=e.slot),i}function je(t,e){for(var n in e)t[_(n)]=e[n]}Se(Ee.prototype);var Ie={init:function(t,e){if(t.componentInstance&&!t.componentInstance._isDestroyed&&t.data.keepAlive){var r=t;Ie.prepatch(r,r)}else{(t.componentInstance=function(t,e){var r={_isComponent:!0,_parentVnode:t,parent:e},o=t.data.inlineTemplate;n(o)&&(r.render=o.render,r.staticRenderFns=o.staticRenderFns);return new t.componentOptions.Ctor(r)}(t,Ke)).$mount(e?t.elm:void 0,e)}},prepatch:function(e,n){var r=n.componentOptions;!function(e,n,r,o,i){var a=o.data.scopedSlots,s=e.$scopedSlots,c=!!(a&&!a.$stable||s!==t&&!s.$stable||a&&e.$scopedSlots.$key!==a.$key||!a&&e.$scopedSlots.$key),u=!!(i||e.$options._renderChildren||c);e.$options._parentVnode=o,e.$vnode=o,e._vnode&&(e._vnode.parent=o);if(e.$options._renderChildren=i,e.$attrs=o.data.attrs||t,e.$listeners=r||t,n&&e.$options.props){_t(!1);for(var l=e._props,f=e.$options._propKeys||[],d=0;d<f.length;d++){var p=f[d],v=e.$options.props;l[p]=Dt(p,v,n,e)}_t(!0),e.$options.propsData=n}r=r||t;var h=e.$options._parentListeners;e.$options._parentListeners=r,qe(e,r,h),u&&(e.$slots=ce(i,o.context),e.$forceUpdate())}(n.componentInstance=e.componentInstance,r.propsData,r.listeners,n,r.children)},insert:function(t){var e,n=t.context,r=t.componentInstance;r._isMounted||(r._isMounted=!0,Je(r,"mounted")),t.data.keepAlive&&(n._isMounted?((e=r)._inactive=!1,Ye.push(e)):Ze(r,!0))},destroy:function(t){var e=t.componentInstance;e._isDestroyed||(t.data.keepAlive?function t(e,n){if(n&&(e._directInactive=!0,Ge(e)))return;if(!e._inactive){e._inactive=!0;for(var r=0;r<e.$children.length;r++)t(e.$children[r]);Je(e,"deactivated")}}(e,!0):e.$destroy())}},De=Object.keys(Ie);function Ne(o,a,s,c,l){if(!e(o)){var f=s.$options._base;if(i(o)&&(o=f.extend(o)),"function"==typeof o){var d;if(e(o.cid)&&void 0===(o=function(t,o){if(r(t.error)&&n(t.errorComp))return t.errorComp;if(n(t.resolved))return t.resolved;var a=Ve;a&&n(t.owners)&&-1===t.owners.indexOf(a)&&t.owners.push(a);if(r(t.loading)&&n(t.loadingComp))return t.loadingComp;if(a&&!n(t.owners)){var s=t.owners=[a],c=!0,l=null,f=null;a.$on("hook:destroyed",function(){return v(s,a)});var d=function(t){for(var e=0,n=s.length;e<n;e++)s[e].$forceUpdate();t&&(s.length=0,null!==l&&(clearTimeout(l),l=null),null!==f&&(clearTimeout(f),f=null))},p=I(function(e){t.resolved=Ue(e,o),c?s.length=0:d(!0)}),h=I(function(e){n(t.errorComp)&&(t.error=!0,d(!0))}),m=t(p,h);return i(m)&&(u(m)?e(t.resolved)&&m.then(p,h):u(m.component)&&(m.component.then(p,h),n(m.error)&&(t.errorComp=Ue(m.error,o)),n(m.loading)&&(t.loadingComp=Ue(m.loading,o),0===m.delay?t.loading=!0:l=setTimeout(function(){l=null,e(t.resolved)&&e(t.error)&&(t.loading=!0,d(!1))},m.delay||200)),n(m.timeout)&&(f=setTimeout(function(){f=null,e(t.resolved)&&h(null)},m.timeout)))),c=!1,t.loading?t.loadingComp:t.resolved}}(d=o,f)))return function(t,e,n,r,o){var i=dt();return i.asyncFactory=t,i.asyncMeta={data:e,context:n,children:r,tag:o},i}(d,a,s,c,l);a=a||{},bn(o),n(a.model)&&function(t,e){var r=t.model&&t.model.prop||"value",o=t.model&&t.model.event||"input";(e.attrs||(e.attrs={}))[r]=e.model.value;var i=e.on||(e.on={}),a=i[o],s=e.model.callback;n(a)?(Array.isArray(a)?-1===a.indexOf(s):a!==s)&&(i[o]=[s].concat(a)):i[o]=s}(o.options,a);var p=function(t,r,o){var i=r.options.props;if(!e(i)){var a={},s=t.attrs,c=t.props;if(n(s)||n(c))for(var u in i){var l=$(u);oe(a,c,u,l,!0)||oe(a,s,u,l,!1)}return a}}(a,o);if(r(o.options.functional))return function(e,r,o,i,a){var s=e.options,c={},u=s.props;if(n(u))for(var l in u)c[l]=Dt(l,u,r||t);else n(o.attrs)&&je(c,o.attrs),n(o.props)&&je(c,o.props);var f=new Ee(o,c,a,i,e),d=s.render.call(null,f._c,f);if(d instanceof lt)return Te(d,o,f.parent,s);if(Array.isArray(d)){for(var p=ie(d)||[],v=new Array(p.length),h=0;h<p.length;h++)v[h]=Te(p[h],o,f.parent,s);return v}}(o,p,a,s,c);var h=a.on;if(a.on=a.nativeOn,r(o.options.abstract)){var m=a.slot;a={},m&&(a.slot=m)}!function(t){for(var e=t.hook||(t.hook={}),n=0;n<De.length;n++){var r=De[n],o=e[r],i=Ie[r];o===i||o&&o._merged||(e[r]=o?Pe(i,o):i)}}(a);var y=o.options.name||l;return new lt("vue-component-"+o.cid+(y?"-"+y:""),a,void 0,void 0,void 0,s,{Ctor:o,propsData:p,listeners:h,tag:l,children:c},d)}}}function Pe(t,e){var n=function(n,r){t(n,r),e(n,r)};return n._merged=!0,n}var Le=1,Me=2;function Fe(t,a,s,c,u,l){return(Array.isArray(s)||o(s))&&(u=c,c=s,s=void 0),r(l)&&(u=Me),function(t,o,a,s,c){if(n(a)&&n(a.__ob__))return dt();n(a)&&n(a.is)&&(o=a.is);if(!o)return dt();Array.isArray(s)&&"function"==typeof s[0]&&((a=a||{}).scopedSlots={default:s[0]},s.length=0);c===Me?s=ie(s):c===Le&&(s=function(t){for(var e=0;e<t.length;e++)if(Array.isArray(t[e]))return Array.prototype.concat.apply([],t);return t}(s));var u,l;if("string"==typeof o){var f;l=t.$vnode&&t.$vnode.ns||L.getTagNamespace(o),u=L.isReservedTag(o)?new lt(L.parsePlatformTagName(o),a,s,void 0,void 0,t):a&&a.pre||!n(f=It(t.$options,"components",o))?new lt(o,a,s,void 0,void 0,t):Ne(f,a,t,s,o)}else u=Ne(o,a,t,s);return Array.isArray(u)?u:n(u)?(n(l)&&function t(o,i,a){o.ns=i;"foreignObject"===o.tag&&(i=void 0,a=!0);if(n(o.children))for(var s=0,c=o.children.length;s<c;s++){var u=o.children[s];n(u.tag)&&(e(u.ns)||r(a)&&"svg"!==u.tag)&&t(u,i,a)}}(u,l),n(a)&&function(t){i(t.style)&&Yt(t.style);i(t.class)&&Yt(t.class)}(a),u):dt()}(t,a,s,c,u)}var Re,Ve=null;function Ue(t,e){return(t.__esModule||rt&&"Module"===t[Symbol.toStringTag])&&(t=t.default),i(t)?e.extend(t):t}function He(t){if(Array.isArray(t))for(var e=0;e<t.length;e++){var r=t[e];if(n(r)&&(n(r.componentOptions)||le(r)))return r}}function Be(t,e){Re.$on(t,e)}function ze(t,e){Re.$off(t,e)}function We(t,e){var n=Re;return function r(){null!==e.apply(null,arguments)&&n.$off(t,r)}}function qe(t,e,n){Re=t,ne(e,n||{},Be,ze,We,t),Re=void 0}var Ke=null;function Xe(t){var e=Ke;return Ke=t,function(){Ke=e}}function Ge(t){for(;t&&(t=t.$parent);)if(t._inactive)return!0;return!1}function Ze(t,e){if(e){if(t._directInactive=!1,Ge(t))return}else if(t._directInactive)return;if(t._inactive||null===t._inactive){t._inactive=!1;for(var n=0;n<t.$children.length;n++)Ze(t.$children[n]);Je(t,"activated")}}function Je(t,e){ct();var n=t.$options[e],r=e+" hook";if(n)for(var o=0,i=n.length;o<i;o++)Rt(n[o],t,null,t,r);t._hasHookEvent&&t.$emit("hook:"+e),ut()}var Qe=[],Ye=[],tn={},en=!1,nn=!1,rn=0;var on=0,an=Date.now;if(U&&!W){var sn=window.performance;sn&&"function"==typeof sn.now&&an()>document.createEvent("Event").timeStamp&&(an=function(){return sn.now()})}function cn(){var t,e;for(on=an(),nn=!0,Qe.sort(function(t,e){return t.id-e.id}),rn=0;rn<Qe.length;rn++)(t=Qe[rn]).before&&t.before(),e=t.id,tn[e]=null,t.run();var n=Ye.slice(),r=Qe.slice();rn=Qe.length=Ye.length=0,tn={},en=nn=!1,function(t){for(var e=0;e<t.length;e++)t[e]._inactive=!0,Ze(t[e],!0)}(n),function(t){var e=t.length;for(;e--;){var n=t[e],r=n.vm;r._watcher===n&&r._isMounted&&!r._isDestroyed&&Je(r,"updated")}}(r),tt&&L.devtools&&tt.emit("flush")}var un=0,ln=function(t,e,n,r,o){this.vm=t,o&&(t._watcher=this),t._watchers.push(this),r?(this.deep=!!r.deep,this.user=!!r.user,this.lazy=!!r.lazy,this.sync=!!r.sync,this.before=r.before):this.deep=this.user=this.lazy=this.sync=!1,this.cb=n,this.id=++un,this.active=!0,this.dirty=this.lazy,this.deps=[],this.newDeps=[],this.depIds=new nt,this.newDepIds=new nt,this.expression="","function"==typeof e?this.getter=e:(this.getter=function(t){if(!F.test(t)){var e=t.split(".");return function(t){for(var n=0;n<e.length;n++){if(!t)return;t=t[e[n]]}return t}}}(e),this.getter||(this.getter=O)),this.value=this.lazy?void 0:this.get()};ln.prototype.get=function(){var t;ct(this);var e=this.vm;try{t=this.getter.call(e,e)}catch(t){if(!this.user)throw t;Ft(t,e,'getter for watcher "'+this.expression+'"')}finally{this.deep&&Yt(t),ut(),this.cleanupDeps()}return t},ln.prototype.addDep=function(t){var e=t.id;this.newDepIds.has(e)||(this.newDepIds.add(e),this.newDeps.push(t),this.depIds.has(e)||t.addSub(this))},ln.prototype.cleanupDeps=function(){for(var t=this.deps.length;t--;){var e=this.deps[t];this.newDepIds.has(e.id)||e.removeSub(this)}var n=this.depIds;this.depIds=this.newDepIds,this.newDepIds=n,this.newDepIds.clear(),n=this.deps,this.deps=this.newDeps,this.newDeps=n,this.newDeps.length=0},ln.prototype.update=function(){this.lazy?this.dirty=!0:this.sync?this.run():function(t){var e=t.id;if(null==tn[e]){if(tn[e]=!0,nn){for(var n=Qe.length-1;n>rn&&Qe[n].id>t.id;)n--;Qe.splice(n+1,0,t)}else Qe.push(t);en||(en=!0,Jt(cn))}}(this)},ln.prototype.run=function(){if(this.active){var t=this.get();if(t!==this.value||i(t)||this.deep){var e=this.value;if(this.value=t,this.user){var n='callback for watcher "'+this.expression+'"';Rt(this.cb,this.vm,[t,e],this.vm,n)}else this.cb.call(this.vm,t,e)}}},ln.prototype.evaluate=function(){this.value=this.get(),this.dirty=!1},ln.prototype.depend=function(){for(var t=this.deps.length;t--;)this.deps[t].depend()},ln.prototype.teardown=function(){if(this.active){this.vm._isBeingDestroyed||v(this.vm._watchers,this);for(var t=this.deps.length;t--;)this.deps[t].removeSub(this);this.active=!1}};var fn={enumerable:!0,configurable:!0,get:O,set:O};function dn(t,e,n){fn.get=function(){return this[e][n]},fn.set=function(t){this[e][n]=t},Object.defineProperty(t,n,fn)}function pn(t){t._watchers=[];var e=t.$options;e.props&&function(t,e){var n=t.$options.propsData||{},r=t._props={},o=t.$options._propKeys=[];t.$parent&&_t(!1);var i=function(i){o.push(i);var a=Dt(i,e,n,t);$t(r,i,a),i in t||dn(t,"_props",i)};for(var a in e)i(a);_t(!0)}(t,e.props),e.methods&&function(t,e){t.$options.props;for(var n in e)t[n]="function"!=typeof e[n]?O:w(e[n],t)}(t,e.methods),e.data?function(t){var e=t.$options.data;s(e=t._data="function"==typeof e?function(t,e){ct();try{return t.call(e,e)}catch(t){return Ft(t,e,"data()"),{}}finally{ut()}}(e,t):e||{})||(e={});var n=Object.keys(e),r=t.$options.props,o=(t.$options.methods,n.length);for(;o--;){var i=n[o];r&&m(r,i)||(a=void 0,36!==(a=(i+"").charCodeAt(0))&&95!==a&&dn(t,"_data",i))}var a;Ct(e,!0)}(t):Ct(t._data={},!0),e.computed&&function(t,e){var n=t._computedWatchers=Object.create(null),r=Y();for(var o in e){var i=e[o],a="function"==typeof i?i:i.get;r||(n[o]=new ln(t,a||O,O,vn)),o in t||hn(t,o,i)}}(t,e.computed),e.watch&&e.watch!==Z&&function(t,e){for(var n in e){var r=e[n];if(Array.isArray(r))for(var o=0;o<r.length;o++)gn(t,n,r[o]);else gn(t,n,r)}}(t,e.watch)}var vn={lazy:!0};function hn(t,e,n){var r=!Y();"function"==typeof n?(fn.get=r?mn(e):yn(n),fn.set=O):(fn.get=n.get?r&&!1!==n.cache?mn(e):yn(n.get):O,fn.set=n.set||O),Object.defineProperty(t,e,fn)}function mn(t){return function(){var e=this._computedWatchers&&this._computedWatchers[t];if(e)return e.dirty&&e.evaluate(),at.target&&e.depend(),e.value}}function yn(t){return function(){return t.call(this,this)}}function gn(t,e,n,r){return s(n)&&(r=n,n=n.handler),"string"==typeof n&&(n=t[n]),t.$watch(e,n,r)}var _n=0;function bn(t){var e=t.options;if(t.super){var n=bn(t.super);if(n!==t.superOptions){t.superOptions=n;var r=function(t){var e,n=t.options,r=t.sealedOptions;for(var o in n)n[o]!==r[o]&&(e||(e={}),e[o]=n[o]);return e}(t);r&&x(t.extendOptions,r),(e=t.options=jt(n,t.extendOptions)).name&&(e.components[e.name]=t)}}return e}function Cn(t){this._init(t)}function $n(t){t.cid=0;var e=1;t.extend=function(t){t=t||{};var n=this,r=n.cid,o=t._Ctor||(t._Ctor={});if(o[r])return o[r];var i=t.name||n.options.name,a=function(t){this._init(t)};return(a.prototype=Object.create(n.prototype)).constructor=a,a.cid=e++,a.options=jt(n.options,t),a.super=n,a.options.props&&function(t){var e=t.options.props;for(var n in e)dn(t.prototype,"_props",n)}(a),a.options.computed&&function(t){var e=t.options.computed;for(var n in e)hn(t.prototype,n,e[n])}(a),a.extend=n.extend,a.mixin=n.mixin,a.use=n.use,N.forEach(function(t){a[t]=n[t]}),i&&(a.options.components[i]=a),a.superOptions=n.options,a.extendOptions=t,a.sealedOptions=x({},a.options),o[r]=a,a}}function wn(t){return t&&(t.Ctor.options.name||t.tag)}function An(t,e){return Array.isArray(t)?t.indexOf(e)>-1:"string"==typeof t?t.split(",").indexOf(e)>-1:(n=t,"[object RegExp]"===a.call(n)&&t.test(e));var n}function xn(t,e){var n=t.cache,r=t.keys,o=t._vnode;for(var i in n){var a=n[i];if(a){var s=a.name;s&&!e(s)&&kn(n,i,r,o)}}}function kn(t,e,n,r){var o=t[e];!o||r&&o.tag===r.tag||o.componentInstance.$destroy(),t[e]=null,v(n,e)}!function(e){e.prototype._init=function(e){var n=this;n._uid=_n++,n._isVue=!0,e&&e._isComponent?function(t,e){var n=t.$options=Object.create(t.constructor.options),r=e._parentVnode;n.parent=e.parent,n._parentVnode=r;var o=r.componentOptions;n.propsData=o.propsData,n._parentListeners=o.listeners,n._renderChildren=o.children,n._componentTag=o.tag,e.render&&(n.render=e.render,n.staticRenderFns=e.staticRenderFns)}(n,e):n.$options=jt(bn(n.constructor),e||{},n),n._renderProxy=n,n._self=n,function(t){var e=t.$options,n=e.parent;if(n&&!e.abstract){for(;n.$options.abstract&&n.$parent;)n=n.$parent;n.$children.push(t)}t.$parent=n,t.$root=n?n.$root:t,t.$children=[],t.$refs={},t._watcher=null,t._inactive=null,t._directInactive=!1,t._isMounted=!1,t._isDestroyed=!1,t._isBeingDestroyed=!1}(n),function(t){t._events=Object.create(null),t._hasHookEvent=!1;var e=t.$options._parentListeners;e&&qe(t,e)}(n),function(e){e._vnode=null,e._staticTrees=null;var n=e.$options,r=e.$vnode=n._parentVnode,o=r&&r.context;e.$slots=ce(n._renderChildren,o),e.$scopedSlots=t,e._c=function(t,n,r,o){return Fe(e,t,n,r,o,!1)},e.$createElement=function(t,n,r,o){return Fe(e,t,n,r,o,!0)};var i=r&&r.data;$t(e,"$attrs",i&&i.attrs||t,null,!0),$t(e,"$listeners",n._parentListeners||t,null,!0)}(n),Je(n,"beforeCreate"),function(t){var e=se(t.$options.inject,t);e&&(_t(!1),Object.keys(e).forEach(function(n){$t(t,n,e[n])}),_t(!0))}(n),pn(n),function(t){var e=t.$options.provide;e&&(t._provided="function"==typeof e?e.call(t):e)}(n),Je(n,"created"),n.$options.el&&n.$mount(n.$options.el)}}(Cn),function(t){var e={get:function(){return this._data}},n={get:function(){return this._props}};Object.defineProperty(t.prototype,"$data",e),Object.defineProperty(t.prototype,"$props",n),t.prototype.$set=wt,t.prototype.$delete=At,t.prototype.$watch=function(t,e,n){if(s(e))return gn(this,t,e,n);(n=n||{}).user=!0;var r=new ln(this,t,e,n);if(n.immediate){var o='callback for immediate watcher "'+r.expression+'"';ct(),Rt(e,this,[r.value],this,o),ut()}return function(){r.teardown()}}}(Cn),function(t){var e=/^hook:/;t.prototype.$on=function(t,n){var r=this;if(Array.isArray(t))for(var o=0,i=t.length;o<i;o++)r.$on(t[o],n);else(r._events[t]||(r._events[t]=[])).push(n),e.test(t)&&(r._hasHookEvent=!0);return r},t.prototype.$once=function(t,e){var n=this;function r(){n.$off(t,r),e.apply(n,arguments)}return r.fn=e,n.$on(t,r),n},t.prototype.$off=function(t,e){var n=this;if(!arguments.length)return n._events=Object.create(null),n;if(Array.isArray(t)){for(var r=0,o=t.length;r<o;r++)n.$off(t[r],e);return n}var i,a=n._events[t];if(!a)return n;if(!e)return n._events[t]=null,n;for(var s=a.length;s--;)if((i=a[s])===e||i.fn===e){a.splice(s,1);break}return n},t.prototype.$emit=function(t){var e=this._events[t];if(e){e=e.length>1?A(e):e;for(var n=A(arguments,1),r='event handler for "'+t+'"',o=0,i=e.length;o<i;o++)Rt(e[o],this,n,this,r)}return this}}(Cn),function(t){t.prototype._update=function(t,e){var n=this,r=n.$el,o=n._vnode,i=Xe(n);n._vnode=t,n.$el=o?n.__patch__(o,t):n.__patch__(n.$el,t,e,!1),i(),r&&(r.__vue__=null),n.$el&&(n.$el.__vue__=n),n.$vnode&&n.$parent&&n.$vnode===n.$parent._vnode&&(n.$parent.$el=n.$el)},t.prototype.$forceUpdate=function(){this._watcher&&this._watcher.update()},t.prototype.$destroy=function(){var t=this;if(!t._isBeingDestroyed){Je(t,"beforeDestroy"),t._isBeingDestroyed=!0;var e=t.$parent;!e||e._isBeingDestroyed||t.$options.abstract||v(e.$children,t),t._watcher&&t._watcher.teardown();for(var n=t._watchers.length;n--;)t._watchers[n].teardown();t._data.__ob__&&t._data.__ob__.vmCount--,t._isDestroyed=!0,t.__patch__(t._vnode,null),Je(t,"destroyed"),t.$off(),t.$el&&(t.$el.__vue__=null),t.$vnode&&(t.$vnode.parent=null)}}}(Cn),function(t){Se(t.prototype),t.prototype.$nextTick=function(t){return Jt(t,this)},t.prototype._render=function(){var t,e=this,n=e.$options,r=n.render,o=n._parentVnode;o&&(e.$scopedSlots=fe(o.data.scopedSlots,e.$slots,e.$scopedSlots)),e.$vnode=o;try{Ve=e,t=r.call(e._renderProxy,e.$createElement)}catch(n){Ft(n,e,"render"),t=e._vnode}finally{Ve=null}return Array.isArray(t)&&1===t.length&&(t=t[0]),t instanceof lt||(t=dt()),t.parent=o,t}}(Cn);var On=[String,RegExp,Array],Sn={KeepAlive:{name:"keep-alive",abstract:!0,props:{include:On,exclude:On,max:[String,Number]},methods:{cacheVNode:function(){var t=this.cache,e=this.keys,n=this.vnodeToCache,r=this.keyToCache;if(n){var o=n.tag,i=n.componentInstance,a=n.componentOptions;t[r]={name:wn(a),tag:o,componentInstance:i},e.push(r),this.max&&e.length>parseInt(this.max)&&kn(t,e[0],e,this._vnode),this.vnodeToCache=null}}},created:function(){this.cache=Object.create(null),this.keys=[]},destroyed:function(){for(var t in this.cache)kn(this.cache,t,this.keys)},mounted:function(){var t=this;this.cacheVNode(),this.$watch("include",function(e){xn(t,function(t){return An(e,t)})}),this.$watch("exclude",function(e){xn(t,function(t){return!An(e,t)})})},updated:function(){this.cacheVNode()},render:function(){var t=this.$slots.default,e=He(t),n=e&&e.componentOptions;if(n){var r=wn(n),o=this.include,i=this.exclude;if(o&&(!r||!An(o,r))||i&&r&&An(i,r))return e;var a=this.cache,s=this.keys,c=null==e.key?n.Ctor.cid+(n.tag?"::"+n.tag:""):e.key;a[c]?(e.componentInstance=a[c].componentInstance,v(s,c),s.push(c)):(this.vnodeToCache=e,this.keyToCache=c),e.data.keepAlive=!0}return e||t&&t[0]}}};!function(t){var e={get:function(){return L}};Object.defineProperty(t,"config",e),t.util={warn:ot,extend:x,mergeOptions:jt,defineReactive:$t},t.set=wt,t.delete=At,t.nextTick=Jt,t.observable=function(t){return Ct(t),t},t.options=Object.create(null),N.forEach(function(e){t.options[e+"s"]=Object.create(null)}),t.options._base=t,x(t.options.components,Sn),function(t){t.use=function(t){var e=this._installedPlugins||(this._installedPlugins=[]);if(e.indexOf(t)>-1)return this;var n=A(arguments,1);return n.unshift(this),"function"==typeof t.install?t.install.apply(t,n):"function"==typeof t&&t.apply(null,n),e.push(t),this}}(t),function(t){t.mixin=function(t){return this.options=jt(this.options,t),this}}(t),$n(t),function(t){N.forEach(function(e){t[e]=function(t,n){return n?("component"===e&&s(n)&&(n.name=n.name||t,n=this.options._base.extend(n)),"directive"===e&&"function"==typeof n&&(n={bind:n,update:n}),this.options[e+"s"][t]=n,n):this.options[e+"s"][t]}})}(t)}(Cn),Object.defineProperty(Cn.prototype,"$isServer",{get:Y}),Object.defineProperty(Cn.prototype,"$ssrContext",{get:function(){return this.$vnode&&this.$vnode.ssrContext}}),Object.defineProperty(Cn,"FunctionalRenderContext",{value:Ee}),Cn.version="2.6.14";var En=d("style,class"),Tn=d("input,textarea,option,select,progress"),jn=d("contenteditable,draggable,spellcheck"),In=d("events,caret,typing,plaintext-only"),Dn=function(t,e){return Fn(e)||"false"===e?"false":"contenteditable"===t&&In(e)?e:"true"},Nn=d("allowfullscreen,async,autofocus,autoplay,checked,compact,controls,declare,default,defaultchecked,defaultmuted,defaultselected,defer,disabled,enabled,formnovalidate,hidden,indeterminate,inert,ismap,itemscope,loop,multiple,muted,nohref,noresize,noshade,novalidate,nowrap,open,pauseonexit,readonly,required,reversed,scoped,seamless,selected,sortable,truespeed,typemustmatch,visible"),Pn="http://www.w3.org/1999/xlink",Ln=function(t){return":"===t.charAt(5)&&"xlink"===t.slice(0,5)},Mn=function(t){return Ln(t)?t.slice(6,t.length):""},Fn=function(t){return null==t||!1===t};function Rn(t){for(var e=t.data,r=t,o=t;n(o.componentInstance);)(o=o.componentInstance._vnode)&&o.data&&(e=Vn(o.data,e));for(;n(r=r.parent);)r&&r.data&&(e=Vn(e,r.data));return function(t,e){if(n(t)||n(e))return Un(t,Hn(e));return""}(e.staticClass,e.class)}function Vn(t,e){return{staticClass:Un(t.staticClass,e.staticClass),class:n(t.class)?[t.class,e.class]:e.class}}function Un(t,e){return t?e?t+" "+e:t:e||""}function Hn(t){return Array.isArray(t)?function(t){for(var e,r="",o=0,i=t.length;o<i;o++)n(e=Hn(t[o]))&&""!==e&&(r&&(r+=" "),r+=e);return r}(t):i(t)?function(t){var e="";for(var n in t)t[n]&&(e&&(e+=" "),e+=n);return e}(t):"string"==typeof t?t:""}var Bn={svg:"http://www.w3.org/2000/svg",math:"http://www.w3.org/1998/Math/MathML"},zn=d("html,body,base,head,link,meta,style,title,address,article,aside,footer,header,h1,h2,h3,h4,h5,h6,hgroup,nav,section,div,dd,dl,dt,figcaption,figure,picture,hr,img,li,main,ol,p,pre,ul,a,b,abbr,bdi,bdo,br,cite,code,data,dfn,em,i,kbd,mark,q,rp,rt,rtc,ruby,s,samp,small,span,strong,sub,sup,time,u,var,wbr,area,audio,map,track,video,embed,object,param,source,canvas,script,noscript,del,ins,caption,col,colgroup,table,thead,tbody,td,th,tr,button,datalist,fieldset,form,input,label,legend,meter,optgroup,option,output,progress,select,textarea,details,dialog,menu,menuitem,summary,content,element,shadow,template,blockquote,iframe,tfoot"),Wn=d("svg,animate,circle,clippath,cursor,defs,desc,ellipse,filter,font-face,foreignobject,g,glyph,image,line,marker,mask,missing-glyph,path,pattern,polygon,polyline,rect,switch,symbol,text,textpath,tspan,use,view",!0),qn=function(t){return zn(t)||Wn(t)};var Kn=Object.create(null);var Xn=d("text,number,password,search,email,tel,url");var Gn=Object.freeze({createElement:function(t,e){var n=document.createElement(t);return"select"!==t?n:(e.data&&e.data.attrs&&void 0!==e.data.attrs.multiple&&n.setAttribute("multiple","multiple"),n)},createElementNS:function(t,e){return document.createElementNS(Bn[t],e)},createTextNode:function(t){return document.createTextNode(t)},createComment:function(t){return document.createComment(t)},insertBefore:function(t,e,n){t.insertBefore(e,n)},removeChild:function(t,e){t.removeChild(e)},appendChild:function(t,e){t.appendChild(e)},parentNode:function(t){return t.parentNode},nextSibling:function(t){return t.nextSibling},tagName:function(t){return t.tagName},setTextContent:function(t,e){t.textContent=e},setStyleScope:function(t,e){t.setAttribute(e,"")}}),Zn={create:function(t,e){Jn(e)},update:function(t,e){t.data.ref!==e.data.ref&&(Jn(t,!0),Jn(e))},destroy:function(t){Jn(t,!0)}};function Jn(t,e){var r=t.data.ref;if(n(r)){var o=t.context,i=t.componentInstance||t.elm,a=o.$refs;e?Array.isArray(a[r])?v(a[r],i):a[r]===i&&(a[r]=void 0):t.data.refInFor?Array.isArray(a[r])?a[r].indexOf(i)<0&&a[r].push(i):a[r]=[i]:a[r]=i}}var Qn=new lt("",{},[]),Yn=["create","activate","update","remove","destroy"];function tr(t,o){return t.key===o.key&&t.asyncFactory===o.asyncFactory&&(t.tag===o.tag&&t.isComment===o.isComment&&n(t.data)===n(o.data)&&function(t,e){if("input"!==t.tag)return!0;var r,o=n(r=t.data)&&n(r=r.attrs)&&r.type,i=n(r=e.data)&&n(r=r.attrs)&&r.type;return o===i||Xn(o)&&Xn(i)}(t,o)||r(t.isAsyncPlaceholder)&&e(o.asyncFactory.error))}function er(t,e,r){var o,i,a={};for(o=e;o<=r;++o)n(i=t[o].key)&&(a[i]=o);return a}var nr={create:rr,update:rr,destroy:function(t){rr(t,Qn)}};function rr(t,e){(t.data.directives||e.data.directives)&&function(t,e){var n,r,o,i=t===Qn,a=e===Qn,s=ir(t.data.directives,t.context),c=ir(e.data.directives,e.context),u=[],l=[];for(n in c)r=s[n],o=c[n],r?(o.oldValue=r.value,o.oldArg=r.arg,sr(o,"update",e,t),o.def&&o.def.componentUpdated&&l.push(o)):(sr(o,"bind",e,t),o.def&&o.def.inserted&&u.push(o));if(u.length){var f=function(){for(var n=0;n<u.length;n++)sr(u[n],"inserted",e,t)};i?re(e,"insert",f):f()}l.length&&re(e,"postpatch",function(){for(var n=0;n<l.length;n++)sr(l[n],"componentUpdated",e,t)});if(!i)for(n in s)c[n]||sr(s[n],"unbind",t,t,a)}(t,e)}var or=Object.create(null);function ir(t,e){var n,r,o=Object.create(null);if(!t)return o;for(n=0;n<t.length;n++)(r=t[n]).modifiers||(r.modifiers=or),o[ar(r)]=r,r.def=It(e.$options,"directives",r.name);return o}function ar(t){return t.rawName||t.name+"."+Object.keys(t.modifiers||{}).join(".")}function sr(t,e,n,r,o){var i=t.def&&t.def[e];if(i)try{i(n.elm,t,n,r,o)}catch(r){Ft(r,n.context,"directive "+t.name+" "+e+" hook")}}var cr=[Zn,nr];function ur(t,r){var o=r.componentOptions;if(!(n(o)&&!1===o.Ctor.options.inheritAttrs||e(t.data.attrs)&&e(r.data.attrs))){var i,a,s=r.elm,c=t.data.attrs||{},u=r.data.attrs||{};for(i in n(u.__ob__)&&(u=r.data.attrs=x({},u)),u)a=u[i],c[i]!==a&&lr(s,i,a,r.data.pre);for(i in(W||K)&&u.value!==c.value&&lr(s,"value",u.value),c)e(u[i])&&(Ln(i)?s.removeAttributeNS(Pn,Mn(i)):jn(i)||s.removeAttribute(i))}}function lr(t,e,n,r){r||t.tagName.indexOf("-")>-1?fr(t,e,n):Nn(e)?Fn(n)?t.removeAttribute(e):(n="allowfullscreen"===e&&"EMBED"===t.tagName?"true":e,t.setAttribute(e,n)):jn(e)?t.setAttribute(e,Dn(e,n)):Ln(e)?Fn(n)?t.removeAttributeNS(Pn,Mn(e)):t.setAttributeNS(Pn,e,n):fr(t,e,n)}function fr(t,e,n){if(Fn(n))t.removeAttribute(e);else{if(W&&!q&&"TEXTAREA"===t.tagName&&"placeholder"===e&&""!==n&&!t.__ieph){var r=function(e){e.stopImmediatePropagation(),t.removeEventListener("input",r)};t.addEventListener("input",r),t.__ieph=!0}t.setAttribute(e,n)}}var dr={create:ur,update:ur};function pr(t,r){var o=r.elm,i=r.data,a=t.data;if(!(e(i.staticClass)&&e(i.class)&&(e(a)||e(a.staticClass)&&e(a.class)))){var s=Rn(r),c=o._transitionClasses;n(c)&&(s=Un(s,Hn(c))),s!==o._prevClass&&(o.setAttribute("class",s),o._prevClass=s)}}var vr,hr={create:pr,update:pr},mr="__r",yr="__c";function gr(t,e,n){var r=vr;return function o(){null!==e.apply(null,arguments)&&Cr(t,o,n,r)}}var _r=Bt&&!(G&&Number(G[1])<=53);function br(t,e,n,r){if(_r){var o=on,i=e;e=i._wrapper=function(t){if(t.target===t.currentTarget||t.timeStamp>=o||t.timeStamp<=0||t.target.ownerDocument!==document)return i.apply(this,arguments)}}vr.addEventListener(t,e,J?{capture:n,passive:r}:n)}function Cr(t,e,n,r){(r||vr).removeEventListener(t,e._wrapper||e,n)}function $r(t,r){if(!e(t.data.on)||!e(r.data.on)){var o=r.data.on||{},i=t.data.on||{};vr=r.elm,function(t){if(n(t[mr])){var e=W?"change":"input";t[e]=[].concat(t[mr],t[e]||[]),delete t[mr]}n(t[yr])&&(t.change=[].concat(t[yr],t.change||[]),delete t[yr])}(o),ne(o,i,br,Cr,gr,r.context),vr=void 0}}var wr,Ar={create:$r,update:$r};function xr(t,r){if(!e(t.data.domProps)||!e(r.data.domProps)){var o,i,a=r.elm,s=t.data.domProps||{},c=r.data.domProps||{};for(o in n(c.__ob__)&&(c=r.data.domProps=x({},c)),s)o in c||(a[o]="");for(o in c){if(i=c[o],"textContent"===o||"innerHTML"===o){if(r.children&&(r.children.length=0),i===s[o])continue;1===a.childNodes.length&&a.removeChild(a.childNodes[0])}if("value"===o&&"PROGRESS"!==a.tagName){a._value=i;var u=e(i)?"":String(i);kr(a,u)&&(a.value=u)}else if("innerHTML"===o&&Wn(a.tagName)&&e(a.innerHTML)){(wr=wr||document.createElement("div")).innerHTML="<svg>"+i+"</svg>";for(var l=wr.firstChild;a.firstChild;)a.removeChild(a.firstChild);for(;l.firstChild;)a.appendChild(l.firstChild)}else if(i!==s[o])try{a[o]=i}catch(t){}}}}function kr(t,e){return!t.composing&&("OPTION"===t.tagName||function(t,e){var n=!0;try{n=document.activeElement!==t}catch(t){}return n&&t.value!==e}(t,e)||function(t,e){var r=t.value,o=t._vModifiers;if(n(o)){if(o.number)return f(r)!==f(e);if(o.trim)return r.trim()!==e.trim()}return r!==e}(t,e))}var Or={create:xr,update:xr},Sr=y(function(t){var e={},n=/:(.+)/;return t.split(/;(?![^(]*\))/g).forEach(function(t){if(t){var r=t.split(n);r.length>1&&(e[r[0].trim()]=r[1].trim())}}),e});function Er(t){var e=Tr(t.style);return t.staticStyle?x(t.staticStyle,e):e}function Tr(t){return Array.isArray(t)?k(t):"string"==typeof t?Sr(t):t}var jr,Ir=/^--/,Dr=/\s*!important$/,Nr=function(t,e,n){if(Ir.test(e))t.style.setProperty(e,n);else if(Dr.test(n))t.style.setProperty($(e),n.replace(Dr,""),"important");else{var r=Lr(e);if(Array.isArray(n))for(var o=0,i=n.length;o<i;o++)t.style[r]=n[o];else t.style[r]=n}},Pr=["Webkit","Moz","ms"],Lr=y(function(t){if(jr=jr||document.createElement("div").style,"filter"!==(t=_(t))&&t in jr)return t;for(var e=t.charAt(0).toUpperCase()+t.slice(1),n=0;n<Pr.length;n++){var r=Pr[n]+e;if(r in jr)return r}});function Mr(t,r){var o=r.data,i=t.data;if(!(e(o.staticStyle)&&e(o.style)&&e(i.staticStyle)&&e(i.style))){var a,s,c=r.elm,u=i.staticStyle,l=i.normalizedStyle||i.style||{},f=u||l,d=Tr(r.data.style)||{};r.data.normalizedStyle=n(d.__ob__)?x({},d):d;var p=function(t,e){var n,r={};if(e)for(var o=t;o.componentInstance;)(o=o.componentInstance._vnode)&&o.data&&(n=Er(o.data))&&x(r,n);(n=Er(t.data))&&x(r,n);for(var i=t;i=i.parent;)i.data&&(n=Er(i.data))&&x(r,n);return r}(r,!0);for(s in f)e(p[s])&&Nr(c,s,"");for(s in p)(a=p[s])!==f[s]&&Nr(c,s,null==a?"":a)}}var Fr={create:Mr,update:Mr},Rr=/\s+/;function Vr(t,e){if(e&&(e=e.trim()))if(t.classList)e.indexOf(" ")>-1?e.split(Rr).forEach(function(e){return t.classList.add(e)}):t.classList.add(e);else{var n=" "+(t.getAttribute("class")||"")+" ";n.indexOf(" "+e+" ")<0&&t.setAttribute("class",(n+e).trim())}}function Ur(t,e){if(e&&(e=e.trim()))if(t.classList)e.indexOf(" ")>-1?e.split(Rr).forEach(function(e){return t.classList.remove(e)}):t.classList.remove(e),t.classList.length||t.removeAttribute("class");else{for(var n=" "+(t.getAttribute("class")||"")+" ",r=" "+e+" ";n.indexOf(r)>=0;)n=n.replace(r," ");(n=n.trim())?t.setAttribute("class",n):t.removeAttribute("class")}}function Hr(t){if(t){if("object"==typeof t){var e={};return!1!==t.css&&x(e,Br(t.name||"v")),x(e,t),e}return"string"==typeof t?Br(t):void 0}}var Br=y(function(t){return{enterClass:t+"-enter",enterToClass:t+"-enter-to",enterActiveClass:t+"-enter-active",leaveClass:t+"-leave",leaveToClass:t+"-leave-to",leaveActiveClass:t+"-leave-active"}}),zr=U&&!q,Wr="transition",qr="animation",Kr="transition",Xr="transitionend",Gr="animation",Zr="animationend";zr&&(void 0===window.ontransitionend&&void 0!==window.onwebkittransitionend&&(Kr="WebkitTransition",Xr="webkitTransitionEnd"),void 0===window.onanimationend&&void 0!==window.onwebkitanimationend&&(Gr="WebkitAnimation",Zr="webkitAnimationEnd"));var Jr=U?window.requestAnimationFrame?window.requestAnimationFrame.bind(window):setTimeout:function(t){return t()};function Qr(t){Jr(function(){Jr(t)})}function Yr(t,e){var n=t._transitionClasses||(t._transitionClasses=[]);n.indexOf(e)<0&&(n.push(e),Vr(t,e))}function to(t,e){t._transitionClasses&&v(t._transitionClasses,e),Ur(t,e)}function eo(t,e,n){var r=ro(t,e),o=r.type,i=r.timeout,a=r.propCount;if(!o)return n();var s=o===Wr?Xr:Zr,c=0,u=function(){t.removeEventListener(s,l),n()},l=function(e){e.target===t&&++c>=a&&u()};setTimeout(function(){c<a&&u()},i+1),t.addEventListener(s,l)}var no=/\b(transform|all)(,|$)/;function ro(t,e){var n,r=window.getComputedStyle(t),o=(r[Kr+"Delay"]||"").split(", "),i=(r[Kr+"Duration"]||"").split(", "),a=oo(o,i),s=(r[Gr+"Delay"]||"").split(", "),c=(r[Gr+"Duration"]||"").split(", "),u=oo(s,c),l=0,f=0;return e===Wr?a>0&&(n=Wr,l=a,f=i.length):e===qr?u>0&&(n=qr,l=u,f=c.length):f=(n=(l=Math.max(a,u))>0?a>u?Wr:qr:null)?n===Wr?i.length:c.length:0,{type:n,timeout:l,propCount:f,hasTransform:n===Wr&&no.test(r[Kr+"Property"])}}function oo(t,e){for(;t.length<e.length;)t=t.concat(t);return Math.max.apply(null,e.map(function(e,n){return io(e)+io(t[n])}))}function io(t){return 1e3*Number(t.slice(0,-1).replace(",","."))}function ao(t,r){var o=t.elm;n(o._leaveCb)&&(o._leaveCb.cancelled=!0,o._leaveCb());var a=Hr(t.data.transition);if(!e(a)&&!n(o._enterCb)&&1===o.nodeType){for(var s=a.css,c=a.type,u=a.enterClass,l=a.enterToClass,d=a.enterActiveClass,p=a.appearClass,v=a.appearToClass,h=a.appearActiveClass,m=a.beforeEnter,y=a.enter,g=a.afterEnter,_=a.enterCancelled,b=a.beforeAppear,C=a.appear,$=a.afterAppear,w=a.appearCancelled,A=a.duration,x=Ke,k=Ke.$vnode;k&&k.parent;)x=k.context,k=k.parent;var O=!x._isMounted||!t.isRootInsert;if(!O||C||""===C){var S=O&&p?p:u,E=O&&h?h:d,T=O&&v?v:l,j=O&&b||m,D=O&&"function"==typeof C?C:y,N=O&&$||g,P=O&&w||_,L=f(i(A)?A.enter:A),M=!1!==s&&!q,F=uo(D),R=o._enterCb=I(function(){M&&(to(o,T),to(o,E)),R.cancelled?(M&&to(o,S),P&&P(o)):N&&N(o),o._enterCb=null});t.data.show||re(t,"insert",function(){var e=o.parentNode,n=e&&e._pending&&e._pending[t.key];n&&n.tag===t.tag&&n.elm._leaveCb&&n.elm._leaveCb(),D&&D(o,R)}),j&&j(o),M&&(Yr(o,S),Yr(o,E),Qr(function(){to(o,S),R.cancelled||(Yr(o,T),F||(co(L)?setTimeout(R,L):eo(o,c,R)))})),t.data.show&&(r&&r(),D&&D(o,R)),M||F||R()}}}function so(t,r){var o=t.elm;n(o._enterCb)&&(o._enterCb.cancelled=!0,o._enterCb());var a=Hr(t.data.transition);if(e(a)||1!==o.nodeType)return r();if(!n(o._leaveCb)){var s=a.css,c=a.type,u=a.leaveClass,l=a.leaveToClass,d=a.leaveActiveClass,p=a.beforeLeave,v=a.leave,h=a.afterLeave,m=a.leaveCancelled,y=a.delayLeave,g=a.duration,_=!1!==s&&!q,b=uo(v),C=f(i(g)?g.leave:g),$=o._leaveCb=I(function(){o.parentNode&&o.parentNode._pending&&(o.parentNode._pending[t.key]=null),_&&(to(o,l),to(o,d)),$.cancelled?(_&&to(o,u),m&&m(o)):(r(),h&&h(o)),o._leaveCb=null});y?y(w):w()}function w(){$.cancelled||(!t.data.show&&o.parentNode&&((o.parentNode._pending||(o.parentNode._pending={}))[t.key]=t),p&&p(o),_&&(Yr(o,u),Yr(o,d),Qr(function(){to(o,u),$.cancelled||(Yr(o,l),b||(co(C)?setTimeout($,C):eo(o,c,$)))})),v&&v(o,$),_||b||$())}}function co(t){return"number"==typeof t&&!isNaN(t)}function uo(t){if(e(t))return!1;var r=t.fns;return n(r)?uo(Array.isArray(r)?r[0]:r):(t._length||t.length)>1}function lo(t,e){!0!==e.data.show&&ao(e)}var fo=function(t){var i,a,s={},c=t.modules,u=t.nodeOps;for(i=0;i<Yn.length;++i)for(s[Yn[i]]=[],a=0;a<c.length;++a)n(c[a][Yn[i]])&&s[Yn[i]].push(c[a][Yn[i]]);function l(t){var e=u.parentNode(t);n(e)&&u.removeChild(e,t)}function f(t,e,o,i,a,c,l){if(n(t.elm)&&n(c)&&(t=c[l]=vt(t)),t.isRootInsert=!a,!function(t,e,o,i){var a=t.data;if(n(a)){var c=n(t.componentInstance)&&a.keepAlive;if(n(a=a.hook)&&n(a=a.init)&&a(t,!1),n(t.componentInstance))return p(t,e),v(o,t.elm,i),r(c)&&function(t,e,r,o){for(var i,a=t;a.componentInstance;)if(a=a.componentInstance._vnode,n(i=a.data)&&n(i=i.transition)){for(i=0;i<s.activate.length;++i)s.activate[i](Qn,a);e.push(a);break}v(r,t.elm,o)}(t,e,o,i),!0}}(t,e,o,i)){var f=t.data,d=t.children,m=t.tag;n(m)?(t.elm=t.ns?u.createElementNS(t.ns,m):u.createElement(m,t),g(t),h(t,d,e),n(f)&&y(t,e),v(o,t.elm,i)):r(t.isComment)?(t.elm=u.createComment(t.text),v(o,t.elm,i)):(t.elm=u.createTextNode(t.text),v(o,t.elm,i))}}function p(t,e){n(t.data.pendingInsert)&&(e.push.apply(e,t.data.pendingInsert),t.data.pendingInsert=null),t.elm=t.componentInstance.$el,m(t)?(y(t,e),g(t)):(Jn(t),e.push(t))}function v(t,e,r){n(t)&&(n(r)?u.parentNode(r)===t&&u.insertBefore(t,e,r):u.appendChild(t,e))}function h(t,e,n){if(Array.isArray(e))for(var r=0;r<e.length;++r)f(e[r],n,t.elm,null,!0,e,r);else o(t.text)&&u.appendChild(t.elm,u.createTextNode(String(t.text)))}function m(t){for(;t.componentInstance;)t=t.componentInstance._vnode;return n(t.tag)}function y(t,e){for(var r=0;r<s.create.length;++r)s.create[r](Qn,t);n(i=t.data.hook)&&(n(i.create)&&i.create(Qn,t),n(i.insert)&&e.push(t))}function g(t){var e;if(n(e=t.fnScopeId))u.setStyleScope(t.elm,e);else for(var r=t;r;)n(e=r.context)&&n(e=e.$options._scopeId)&&u.setStyleScope(t.elm,e),r=r.parent;n(e=Ke)&&e!==t.context&&e!==t.fnContext&&n(e=e.$options._scopeId)&&u.setStyleScope(t.elm,e)}function _(t,e,n,r,o,i){for(;r<=o;++r)f(n[r],i,t,e,!1,n,r)}function b(t){var e,r,o=t.data;if(n(o))for(n(e=o.hook)&&n(e=e.destroy)&&e(t),e=0;e<s.destroy.length;++e)s.destroy[e](t);if(n(e=t.children))for(r=0;r<t.children.length;++r)b(t.children[r])}function C(t,e,r){for(;e<=r;++e){var o=t[e];n(o)&&(n(o.tag)?($(o),b(o)):l(o.elm))}}function $(t,e){if(n(e)||n(t.data)){var r,o=s.remove.length+1;for(n(e)?e.listeners+=o:e=function(t,e){function n(){0==--n.listeners&&l(t)}return n.listeners=e,n}(t.elm,o),n(r=t.componentInstance)&&n(r=r._vnode)&&n(r.data)&&$(r,e),r=0;r<s.remove.length;++r)s.remove[r](t,e);n(r=t.data.hook)&&n(r=r.remove)?r(t,e):e()}else l(t.elm)}function w(t,e,r,o){for(var i=r;i<o;i++){var a=e[i];if(n(a)&&tr(t,a))return i}}function A(t,o,i,a,c,l){if(t!==o){n(o.elm)&&n(a)&&(o=a[c]=vt(o));var d=o.elm=t.elm;if(r(t.isAsyncPlaceholder))n(o.asyncFactory.resolved)?O(t.elm,o,i):o.isAsyncPlaceholder=!0;else if(r(o.isStatic)&&r(t.isStatic)&&o.key===t.key&&(r(o.isCloned)||r(o.isOnce)))o.componentInstance=t.componentInstance;else{var p,v=o.data;n(v)&&n(p=v.hook)&&n(p=p.prepatch)&&p(t,o);var h=t.children,y=o.children;if(n(v)&&m(o)){for(p=0;p<s.update.length;++p)s.update[p](t,o);n(p=v.hook)&&n(p=p.update)&&p(t,o)}e(o.text)?n(h)&&n(y)?h!==y&&function(t,r,o,i,a){for(var s,c,l,d=0,p=0,v=r.length-1,h=r[0],m=r[v],y=o.length-1,g=o[0],b=o[y],$=!a;d<=v&&p<=y;)e(h)?h=r[++d]:e(m)?m=r[--v]:tr(h,g)?(A(h,g,i,o,p),h=r[++d],g=o[++p]):tr(m,b)?(A(m,b,i,o,y),m=r[--v],b=o[--y]):tr(h,b)?(A(h,b,i,o,y),$&&u.insertBefore(t,h.elm,u.nextSibling(m.elm)),h=r[++d],b=o[--y]):tr(m,g)?(A(m,g,i,o,p),$&&u.insertBefore(t,m.elm,h.elm),m=r[--v],g=o[++p]):(e(s)&&(s=er(r,d,v)),e(c=n(g.key)?s[g.key]:w(g,r,d,v))?f(g,i,t,h.elm,!1,o,p):tr(l=r[c],g)?(A(l,g,i,o,p),r[c]=void 0,$&&u.insertBefore(t,l.elm,h.elm)):f(g,i,t,h.elm,!1,o,p),g=o[++p]);d>v?_(t,e(o[y+1])?null:o[y+1].elm,o,p,y,i):p>y&&C(r,d,v)}(d,h,y,i,l):n(y)?(n(t.text)&&u.setTextContent(d,""),_(d,null,y,0,y.length-1,i)):n(h)?C(h,0,h.length-1):n(t.text)&&u.setTextContent(d,""):t.text!==o.text&&u.setTextContent(d,o.text),n(v)&&n(p=v.hook)&&n(p=p.postpatch)&&p(t,o)}}}function x(t,e,o){if(r(o)&&n(t.parent))t.parent.data.pendingInsert=e;else for(var i=0;i<e.length;++i)e[i].data.hook.insert(e[i])}var k=d("attrs,class,staticClass,staticStyle,key");function O(t,e,o,i){var a,s=e.tag,c=e.data,u=e.children;if(i=i||c&&c.pre,e.elm=t,r(e.isComment)&&n(e.asyncFactory))return e.isAsyncPlaceholder=!0,!0;if(n(c)&&(n(a=c.hook)&&n(a=a.init)&&a(e,!0),n(a=e.componentInstance)))return p(e,o),!0;if(n(s)){if(n(u))if(t.hasChildNodes())if(n(a=c)&&n(a=a.domProps)&&n(a=a.innerHTML)){if(a!==t.innerHTML)return!1}else{for(var l=!0,f=t.firstChild,d=0;d<u.length;d++){if(!f||!O(f,u[d],o,i)){l=!1;break}f=f.nextSibling}if(!l||f)return!1}else h(e,u,o);if(n(c)){var v=!1;for(var m in c)if(!k(m)){v=!0,y(e,o);break}!v&&c.class&&Yt(c.class)}}else t.data!==e.text&&(t.data=e.text);return!0}return function(t,o,i,a){if(!e(o)){var c,l=!1,d=[];if(e(t))l=!0,f(o,d);else{var p=n(t.nodeType);if(!p&&tr(t,o))A(t,o,d,null,null,a);else{if(p){if(1===t.nodeType&&t.hasAttribute(D)&&(t.removeAttribute(D),i=!0),r(i)&&O(t,o,d))return x(o,d,!0),t;c=t,t=new lt(u.tagName(c).toLowerCase(),{},[],void 0,c)}var v=t.elm,h=u.parentNode(v);if(f(o,d,v._leaveCb?null:h,u.nextSibling(v)),n(o.parent))for(var y=o.parent,g=m(o);y;){for(var _=0;_<s.destroy.length;++_)s.destroy[_](y);if(y.elm=o.elm,g){for(var $=0;$<s.create.length;++$)s.create[$](Qn,y);var w=y.data.hook.insert;if(w.merged)for(var k=1;k<w.fns.length;k++)w.fns[k]()}else Jn(y);y=y.parent}n(h)?C([t],0,0):n(t.tag)&&b(t)}}return x(o,d,l),o.elm}n(t)&&b(t)}}({nodeOps:Gn,modules:[dr,hr,Ar,Or,Fr,U?{create:lo,activate:lo,remove:function(t,e){!0!==t.data.show?so(t,e):e()}}:{}].concat(cr)});q&&document.addEventListener("selectionchange",function(){var t=document.activeElement;t&&t.vmodel&&bo(t,"input")});var po={inserted:function(t,e,n,r){"select"===n.tag?(r.elm&&!r.elm._vOptions?re(n,"postpatch",function(){po.componentUpdated(t,e,n)}):vo(t,e,n.context),t._vOptions=[].map.call(t.options,yo)):("textarea"===n.tag||Xn(t.type))&&(t._vModifiers=e.modifiers,e.modifiers.lazy||(t.addEventListener("compositionstart",go),t.addEventListener("compositionend",_o),t.addEventListener("change",_o),q&&(t.vmodel=!0)))},componentUpdated:function(t,e,n){if("select"===n.tag){vo(t,e,n.context);var r=t._vOptions,o=t._vOptions=[].map.call(t.options,yo);if(o.some(function(t,e){return!T(t,r[e])}))(t.multiple?e.value.some(function(t){return mo(t,o)}):e.value!==e.oldValue&&mo(e.value,o))&&bo(t,"change")}}};function vo(t,e,n){ho(t,e,n),(W||K)&&setTimeout(function(){ho(t,e,n)},0)}function ho(t,e,n){var r=e.value,o=t.multiple;if(!o||Array.isArray(r)){for(var i,a,s=0,c=t.options.length;s<c;s++)if(a=t.options[s],o)i=j(r,yo(a))>-1,a.selected!==i&&(a.selected=i);else if(T(yo(a),r))return void(t.selectedIndex!==s&&(t.selectedIndex=s));o||(t.selectedIndex=-1)}}function mo(t,e){return e.every(function(e){return!T(e,t)})}function yo(t){return"_value"in t?t._value:t.value}function go(t){t.target.composing=!0}function _o(t){t.target.composing&&(t.target.composing=!1,bo(t.target,"input"))}function bo(t,e){var n=document.createEvent("HTMLEvents");n.initEvent(e,!0,!0),t.dispatchEvent(n)}function Co(t){return!t.componentInstance||t.data&&t.data.transition?t:Co(t.componentInstance._vnode)}var $o={model:po,show:{bind:function(t,e,n){var r=e.value,o=(n=Co(n)).data&&n.data.transition,i=t.__vOriginalDisplay="none"===t.style.display?"":t.style.display;r&&o?(n.data.show=!0,ao(n,function(){t.style.display=i})):t.style.display=r?i:"none"},update:function(t,e,n){var r=e.value;!r!=!e.oldValue&&((n=Co(n)).data&&n.data.transition?(n.data.show=!0,r?ao(n,function(){t.style.display=t.__vOriginalDisplay}):so(n,function(){t.style.display="none"})):t.style.display=r?t.__vOriginalDisplay:"none")},unbind:function(t,e,n,r,o){o||(t.style.display=t.__vOriginalDisplay)}}},wo={name:String,appear:Boolean,css:Boolean,mode:String,type:String,enterClass:String,leaveClass:String,enterToClass:String,leaveToClass:String,enterActiveClass:String,leaveActiveClass:String,appearClass:String,appearActiveClass:String,appearToClass:String,duration:[Number,String,Object]};function Ao(t){var e=t&&t.componentOptions;return e&&e.Ctor.options.abstract?Ao(He(e.children)):t}function xo(t){var e={},n=t.$options;for(var r in n.propsData)e[r]=t[r];var o=n._parentListeners;for(var i in o)e[_(i)]=o[i];return e}function ko(t,e){if(/\d-keep-alive$/.test(e.tag))return t("keep-alive",{props:e.componentOptions.propsData})}var Oo=function(t){return t.tag||le(t)},So=function(t){return"show"===t.name},Eo={name:"transition",props:wo,abstract:!0,render:function(t){var e=this,n=this.$slots.default;if(n&&(n=n.filter(Oo)).length){var r=this.mode,i=n[0];if(function(t){for(;t=t.parent;)if(t.data.transition)return!0}(this.$vnode))return i;var a=Ao(i);if(!a)return i;if(this._leaving)return ko(t,i);var s="__transition-"+this._uid+"-";a.key=null==a.key?a.isComment?s+"comment":s+a.tag:o(a.key)?0===String(a.key).indexOf(s)?a.key:s+a.key:a.key;var c=(a.data||(a.data={})).transition=xo(this),u=this._vnode,l=Ao(u);if(a.data.directives&&a.data.directives.some(So)&&(a.data.show=!0),l&&l.data&&!function(t,e){return e.key===t.key&&e.tag===t.tag}(a,l)&&!le(l)&&(!l.componentInstance||!l.componentInstance._vnode.isComment)){var f=l.data.transition=x({},c);if("out-in"===r)return this._leaving=!0,re(f,"afterLeave",function(){e._leaving=!1,e.$forceUpdate()}),ko(t,i);if("in-out"===r){if(le(a))return u;var d,p=function(){d()};re(c,"afterEnter",p),re(c,"enterCancelled",p),re(f,"delayLeave",function(t){d=t})}}return i}}},To=x({tag:String,moveClass:String},wo);function jo(t){t.elm._moveCb&&t.elm._moveCb(),t.elm._enterCb&&t.elm._enterCb()}function Io(t){t.data.newPos=t.elm.getBoundingClientRect()}function Do(t){var e=t.data.pos,n=t.data.newPos,r=e.left-n.left,o=e.top-n.top;if(r||o){t.data.moved=!0;var i=t.elm.style;i.transform=i.WebkitTransform="translate("+r+"px,"+o+"px)",i.transitionDuration="0s"}}delete To.mode;var No={Transition:Eo,TransitionGroup:{props:To,beforeMount:function(){var t=this,e=this._update;this._update=function(n,r){var o=Xe(t);t.__patch__(t._vnode,t.kept,!1,!0),t._vnode=t.kept,o(),e.call(t,n,r)}},render:function(t){for(var e=this.tag||this.$vnode.data.tag||"span",n=Object.create(null),r=this.prevChildren=this.children,o=this.$slots.default||[],i=this.children=[],a=xo(this),s=0;s<o.length;s++){var c=o[s];c.tag&&null!=c.key&&0!==String(c.key).indexOf("__vlist")&&(i.push(c),n[c.key]=c,(c.data||(c.data={})).transition=a)}if(r){for(var u=[],l=[],f=0;f<r.length;f++){var d=r[f];d.data.transition=a,d.data.pos=d.elm.getBoundingClientRect(),n[d.key]?u.push(d):l.push(d)}this.kept=t(e,null,u),this.removed=l}return t(e,null,i)},updated:function(){var t=this.prevChildren,e=this.moveClass||(this.name||"v")+"-move";t.length&&this.hasMove(t[0].elm,e)&&(t.forEach(jo),t.forEach(Io),t.forEach(Do),this._reflow=document.body.offsetHeight,t.forEach(function(t){if(t.data.moved){var n=t.elm,r=n.style;Yr(n,e),r.transform=r.WebkitTransform=r.transitionDuration="",n.addEventListener(Xr,n._moveCb=function t(r){r&&r.target!==n||r&&!/transform$/.test(r.propertyName)||(n.removeEventListener(Xr,t),n._moveCb=null,to(n,e))})}}))},methods:{hasMove:function(t,e){if(!zr)return!1;if(this._hasMove)return this._hasMove;var n=t.cloneNode();t._transitionClasses&&t._transitionClasses.forEach(function(t){Ur(n,t)}),Vr(n,e),n.style.display="none",this.$el.appendChild(n);var r=ro(n);return this.$el.removeChild(n),this._hasMove=r.hasTransform}}}};return Cn.config.mustUseProp=function(t,e,n){return"value"===n&&Tn(t)&&"button"!==e||"selected"===n&&"option"===t||"checked"===n&&"input"===t||"muted"===n&&"video"===t},Cn.config.isReservedTag=qn,Cn.config.isReservedAttr=En,Cn.config.getTagNamespace=function(t){return Wn(t)?"svg":"math"===t?"math":void 0},Cn.config.isUnknownElement=function(t){if(!U)return!0;if(qn(t))return!1;if(t=t.toLowerCase(),null!=Kn[t])return Kn[t];var e=document.createElement(t);return t.indexOf("-")>-1?Kn[t]=e.constructor===window.HTMLUnknownElement||e.constructor===window.HTMLElement:Kn[t]=/HTMLUnknownElement/.test(e.toString())},x(Cn.options.directives,$o),x(Cn.options.components,No),Cn.prototype.__patch__=U?fo:O,Cn.prototype.$mount=function(t,e){return function(t,e,n){var r;return t.$el=e,t.$options.render||(t.$options.render=dt),Je(t,"beforeMount"),r=function(){t._update(t._render(),n)},new ln(t,r,O,{before:function(){t._isMounted&&!t._isDestroyed&&Je(t,"beforeUpdate")}},!0),n=!1,null==t.$vnode&&(t._isMounted=!0,Je(t,"mounted")),t}(this,t=t&&U?function(t){if("string"==typeof t){var e=document.querySelector(t);return e||document.createElement("div")}return t}(t):void 0,e)},U&&setTimeout(function(){L.devtools&&tt&&tt.emit("init",Cn)},0),Cn});</script><script h5only type="text/javascript" nonce="1682091926" reportloaderror>(function(e,t){"object"===typeof exports&&"object"===typeof module?module.exports=t():"function"===typeof define&&define.amd?define([],t):"object"===typeof exports?exports["weEmoji"]=t():e["weEmoji"]=t()})("undefined"!==typeof self?self:this,(function(){return function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s="fb15")}({"00ee":function(e,t,n){var r=n("b622"),o=r("toStringTag"),i={};i[o]="z",e.exports="[object z]"===String(i)},"0366":function(e,t,n){var r=n("1c0b");e.exports=function(e,t,n){if(r(e),void 0===t)return e;switch(n){case 0:return function(){return e.call(t)};case 1:return function(n){return e.call(t,n)};case 2:return function(n,r){return e.call(t,n,r)};case 3:return function(n,r,o){return e.call(t,n,r,o)}}return function(){return e.apply(t,arguments)}}},"057f":function(e,t,n){var r=n("fc6a"),o=n("241c").f,i={}.toString,s="object"==typeof window&&window&&Object.getOwnPropertyNames?Object.getOwnPropertyNames(window):[],a=function(e){try{return o(e)}catch(t){return s.slice()}};e.exports.f=function(e){return s&&"[object Window]"==i.call(e)?a(e):o(r(e))}},"06cf":function(e,t,n){var r=n("83ab"),o=n("d1e7"),i=n("5c6c"),s=n("fc6a"),a=n("c04e"),c=n("5135"),u=n("0cfb"),p=Object.getOwnPropertyDescriptor;t.f=r?p:function(e,t){if(e=s(e),t=a(t,!0),u)try{return p(e,t)}catch(n){}if(c(e,t))return i(!o.f.call(e,t),e[t])}},"07ac":function(e,t,n){var r=n("23e7"),o=n("6f53").values;r({target:"Object",stat:!0},{values:function(e){return o(e)}})},"0cb2":function(e,t,n){var r=n("7b0b"),o=Math.floor,i="".replace,s=/\$([$&'`]|\d{1,2}|<[^>]*>)/g,a=/\$([$&'`]|\d{1,2})/g;e.exports=function(e,t,n,c,u,p){var f=n+e.length,l=c.length,h=a;return void 0!==u&&(u=r(u),h=s),i.call(p,h,(function(r,i){var s;switch(i.charAt(0)){case"$":return"$";case"&":return e;case"`":return t.slice(0,n);case"'":return t.slice(f);case"<":s=u[i.slice(1,-1)];break;default:var a=+i;if(0===a)return r;if(a>l){var p=o(a/10);return 0===p?r:p<=l?void 0===c[p-1]?i.charAt(1):c[p-1]+i.charAt(1):r}s=c[a-1]}return void 0===s?"":s}))}},"0cfb":function(e,t,n){var r=n("83ab"),o=n("d039"),i=n("cc12");e.exports=!r&&!o((function(){return 7!=Object.defineProperty(i("div"),"a",{get:function(){return 7}}).a}))},"13d5":function(e,t,n){"use strict";var r=n("23e7"),o=n("d58f").left,i=n("a640"),s=n("2d00"),a=n("605d"),c=i("reduce"),u=!a&&s>79&&s<83;r({target:"Array",proto:!0,forced:!c||u},{reduce:function(e){return o(this,e,arguments.length,arguments.length>1?arguments[1]:void 0)}})},"14c3":function(e,t,n){var r=n("c6b6"),o=n("9263");e.exports=function(e,t){var n=e.exec;if("function"===typeof n){var i=n.call(e,t);if("object"!==typeof i)throw TypeError("RegExp exec method returned something other than an Object or null");return i}if("RegExp"!==r(e))throw TypeError("RegExp#exec called on incompatible receiver");return o.call(e,t)}},"159b":function(e,t,n){var r=n("da84"),o=n("fdbc"),i=n("17c2"),s=n("9112");for(var a in o){var c=r[a],u=c&&c.prototype;if(u&&u.forEach!==i)try{s(u,"forEach",i)}catch(p){u.forEach=i}}},"17c2":function(e,t,n){"use strict";var r=n("b727").forEach,o=n("a640"),i=o("forEach");e.exports=i?[].forEach:function(e){return r(this,e,arguments.length>1?arguments[1]:void 0)}},"1be4":function(e,t,n){var r=n("d066");e.exports=r("document","documentElement")},"1c0b":function(e,t){e.exports=function(e){if("function"!=typeof e)throw TypeError(String(e)+" is not a function");return e}},"1c7e":function(e,t,n){var r=n("b622"),o=r("iterator"),i=!1;try{var s=0,a={next:function(){return{done:!!s++}},return:function(){i=!0}};a[o]=function(){return this},Array.from(a,(function(){throw 2}))}catch(c){}e.exports=function(e,t){if(!t&&!i)return!1;var n=!1;try{var r={};r[o]=function(){return{next:function(){return{done:n=!0}}}},e(r)}catch(c){}return n}},"1d80":function(e,t){e.exports=function(e){if(void 0==e)throw TypeError("Can't call method on "+e);return e}},"1dde":function(e,t,n){var r=n("d039"),o=n("b622"),i=n("2d00"),s=o("species");e.exports=function(e){return i>=51||!r((function(){var t=[],n=t.constructor={};return n[s]=function(){return{foo:1}},1!==t[e](Boolean).foo}))}},"23cb":function(e,t,n){var r=n("a691"),o=Math.max,i=Math.min;e.exports=function(e,t){var n=r(e);return n<0?o(n+t,0):i(n,t)}},"23e7":function(e,t,n){var r=n("da84"),o=n("06cf").f,i=n("9112"),s=n("6eeb"),a=n("ce4e"),c=n("e893"),u=n("94ca");e.exports=function(e,t){var n,p,f,l,h,d,y=e.target,x=e.global,m=e.stat;if(p=x?r:m?r[y]||a(y,{}):(r[y]||{}).prototype,p)for(f in t){if(h=t[f],e.noTargetGet?(d=o(p,f),l=d&&d.value):l=p[f],n=u(x?f:y+(m?".":"#")+f,e.forced),!n&&void 0!==l){if(typeof h===typeof l)continue;c(h,l)}(e.sham||l&&l.sham)&&i(h,"sham",!0),s(p,f,h,e)}}},"241c":function(e,t,n){var r=n("ca84"),o=n("7839"),i=o.concat("length","prototype");t.f=Object.getOwnPropertyNames||function(e){return r(e,i)}},"25f0":function(e,t,n){"use strict";var r=n("6eeb"),o=n("825a"),i=n("d039"),s=n("ad6d"),a="toString",c=RegExp.prototype,u=c[a],p=i((function(){return"/a/b"!=u.call({source:"a",flags:"b"})})),f=u.name!=a;(p||f)&&r(RegExp.prototype,a,(function(){var e=o(this),t=String(e.source),n=e.flags,r=String(void 0===n&&e instanceof RegExp&&!("flags"in c)?s.call(e):n);return"/"+t+"/"+r}),{unsafe:!0})},2626:function(e,t,n){"use strict";var r=n("d066"),o=n("9bf2"),i=n("b622"),s=n("83ab"),a=i("species");e.exports=function(e){var t=r(e),n=o.f;s&&t&&!t[a]&&n(t,a,{configurable:!0,get:function(){return this}})}},"2a62":function(e,t,n){var r=n("825a");e.exports=function(e){var t=e["return"];if(void 0!==t)return r(t.call(e)).value}},"2d00":function(e,t,n){var r,o,i=n("da84"),s=n("342f"),a=i.process,c=a&&a.versions,u=c&&c.v8;u?(r=u.split("."),o=r[0]+r[1]):s&&(r=s.match(/Edge\/(\d+)/),(!r||r[1]>=74)&&(r=s.match(/Chrome\/(\d+)/),r&&(o=r[1]))),e.exports=o&&+o},"342f":function(e,t,n){var r=n("d066");e.exports=r("navigator","userAgent")||""},"35a1":function(e,t,n){var r=n("f5df"),o=n("3f8c"),i=n("b622"),s=i("iterator");e.exports=function(e){if(void 0!=e)return e[s]||e["@@iterator"]||o[r(e)]}},"37e8":function(e,t,n){var r=n("83ab"),o=n("9bf2"),i=n("825a"),s=n("df75");e.exports=r?Object.defineProperties:function(e,t){i(e);var n,r=s(t),a=r.length,c=0;while(a>c)o.f(e,n=r[c++],t[n]);return e}},"3bbe":function(e,t,n){var r=n("861d");e.exports=function(e){if(!r(e)&&null!==e)throw TypeError("Can't set "+String(e)+" as a prototype");return e}},"3ca3":function(e,t,n){"use strict";var r=n("6547").charAt,o=n("69f3"),i=n("7dd0"),s="String Iterator",a=o.set,c=o.getterFor(s);i(String,"String",(function(e){a(this,{type:s,string:String(e),index:0})}),(function(){var e,t=c(this),n=t.string,o=t.index;return o>=n.length?{value:void 0,done:!0}:(e=r(n,o),t.index+=e.length,{value:e,done:!1})}))},"3f8c":function(e,t){e.exports={}},"428f":function(e,t,n){var r=n("da84");e.exports=r},"44ad":function(e,t,n){var r=n("d039"),o=n("c6b6"),i="".split;e.exports=r((function(){return!Object("z").propertyIsEnumerable(0)}))?function(e){return"String"==o(e)?i.call(e,""):Object(e)}:Object},"44d2":function(e,t,n){var r=n("b622"),o=n("7c73"),i=n("9bf2"),s=r("unscopables"),a=Array.prototype;void 0==a[s]&&i.f(a,s,{configurable:!0,value:o(null)}),e.exports=function(e){a[s][e]=!0}},"44e7":function(e,t,n){var r=n("861d"),o=n("c6b6"),i=n("b622"),s=i("match");e.exports=function(e){var t;return r(e)&&(void 0!==(t=e[s])?!!t:"RegExp"==o(e))}},4930:function(e,t,n){var r=n("605d"),o=n("2d00"),i=n("d039");e.exports=!!Object.getOwnPropertySymbols&&!i((function(){return!Symbol.sham&&(r?38===o:o>37&&o<41)}))},"498a":function(e,t,n){"use strict";var r=n("23e7"),o=n("58a8").trim,i=n("c8d2");r({target:"String",proto:!0,forced:i("trim")},{trim:function(){return o(this)}})},"4d63":function(e,t,n){var r=n("83ab"),o=n("da84"),i=n("94ca"),s=n("7156"),a=n("9bf2").f,c=n("241c").f,u=n("44e7"),p=n("ad6d"),f=n("9f7f"),l=n("6eeb"),h=n("d039"),d=n("69f3").set,y=n("2626"),x=n("b622"),m=x("match"),g=o.RegExp,w=g.prototype,_=/a/g,v=/a/g,b=new g(_)!==_,E=f.UNSUPPORTED_Y,j=r&&i("RegExp",!b||E||h((function(){return v[m]=!1,g(_)!=_||g(v)==v||"/a/i"!=g(_,"i")})));if(j){var k=function(e,t){var n,r=this instanceof k,o=u(e),i=void 0===t;if(!r&&o&&e.constructor===k&&i)return e;b?o&&!i&&(e=e.source):e instanceof k&&(i&&(t=p.call(e)),e=e.source),E&&(n=!!t&&t.indexOf("y")>-1,n&&(t=t.replace(/y/g,"")));var a=s(b?new g(e,t):g(e,t),r?this:w,k);return E&&n&&d(a,{sticky:n}),a},S=function(e){e in k||a(k,e,{configurable:!0,get:function(){return g[e]},set:function(t){g[e]=t}})},O=c(g),P=0;while(O.length>P)S(O[P++]);w.constructor=k,k.prototype=w,l(o,"RegExp",k)}y("RegExp")},"4d64":function(e,t,n){var r=n("fc6a"),o=n("50c4"),i=n("23cb"),s=function(e){return function(t,n,s){var a,c=r(t),u=o(c.length),p=i(s,u);if(e&&n!=n){while(u>p)if(a=c[p++],a!=a)return!0}else for(;u>p;p++)if((e||p in c)&&c[p]===n)return e||p||0;return!e&&-1}};e.exports={includes:s(!0),indexOf:s(!1)}},"4de4":function(e,t,n){"use strict";var r=n("23e7"),o=n("b727").filter,i=n("1dde"),s=i("filter");r({target:"Array",proto:!0,forced:!s},{filter:function(e){return o(this,e,arguments.length>1?arguments[1]:void 0)}})},"4df4":function(e,t,n){"use strict";var r=n("0366"),o=n("7b0b"),i=n("9bdd"),s=n("e95a"),a=n("50c4"),c=n("8418"),u=n("35a1");e.exports=function(e){var t,n,p,f,l,h,d=o(e),y="function"==typeof this?this:Array,x=arguments.length,m=x>1?arguments[1]:void 0,g=void 0!==m,w=u(d),_=0;if(g&&(m=r(m,x>2?arguments[2]:void 0,2)),void 0==w||y==Array&&s(w))for(t=a(d.length),n=new y(t);t>_;_++)h=g?m(d[_],_):d[_],c(n,_,h);else for(f=w.call(d),l=f.next,n=new y;!(p=l.call(f)).done;_++)h=g?i(f,m,[p.value,_],!0):p.value,c(n,_,h);return n.length=_,n}},"50c4":function(e,t,n){var r=n("a691"),o=Math.min;e.exports=function(e){return e>0?o(r(e),9007199254740991):0}},5135:function(e,t){var n={}.hasOwnProperty;e.exports=function(e,t){return n.call(e,t)}},5319:function(e,t,n){"use strict";var r=n("d784"),o=n("825a"),i=n("50c4"),s=n("a691"),a=n("1d80"),c=n("8aa5"),u=n("0cb2"),p=n("14c3"),f=Math.max,l=Math.min,h=function(e){return void 0===e?e:String(e)};r("replace",2,(function(e,t,n,r){var d=r.REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE,y=r.REPLACE_KEEPS_$0,x=d?"$":"$0";return[function(n,r){var o=a(this),i=void 0==n?void 0:n[e];return void 0!==i?i.call(n,o,r):t.call(String(o),n,r)},function(e,r){if(!d&&y||"string"===typeof r&&-1===r.indexOf(x)){var a=n(t,e,this,r);if(a.done)return a.value}var m=o(e),g=String(this),w="function"===typeof r;w||(r=String(r));var _=m.global;if(_){var v=m.unicode;m.lastIndex=0}var b=[];while(1){var E=p(m,g);if(null===E)break;if(b.push(E),!_)break;var j=String(E[0]);""===j&&(m.lastIndex=c(g,i(m.lastIndex),v))}for(var k="",S=0,O=0;O<b.length;O++){E=b[O];for(var P=String(E[0]),T=f(l(s(E.index),g.length),0),D=[],q=1;q<E.length;q++)D.push(h(E[q]));var A=E.groups;if(w){var R=[P].concat(D,T,g);void 0!==A&&R.push(A);var C=String(r.apply(void 0,R))}else C=u(P,g,T,D,A,r);T>=S&&(k+=g.slice(S,T)+C,S=T+P.length)}return k+g.slice(S)}]}))},5692:function(e,t,n){var r=n("c430"),o=n("c6cd");(e.exports=function(e,t){return o[e]||(o[e]=void 0!==t?t:{})})("versions",[]).push({version:"3.9.1",mode:r?"pure":"global",copyright:"© 2021 Denis Pushkarev (zloirock.ru)"})},"56ef":function(e,t,n){var r=n("d066"),o=n("241c"),i=n("7418"),s=n("825a");e.exports=r("Reflect","ownKeys")||function(e){var t=o.f(s(e)),n=i.f;return n?t.concat(n(e)):t}},5899:function(e,t){e.exports="\t\n\v\f\r                　\u2028\u2029\ufeff"},"58a8":function(e,t,n){var r=n("1d80"),o=n("5899"),i="["+o+"]",s=RegExp("^"+i+i+"*"),a=RegExp(i+i+"*$"),c=function(e){return function(t){var n=String(r(t));return 1&e&&(n=n.replace(s,"")),2&e&&(n=n.replace(a,"")),n}};e.exports={start:c(1),end:c(2),trim:c(3)}},"5c6c":function(e,t){e.exports=function(e,t){return{enumerable:!(1&e),configurable:!(2&e),writable:!(4&e),value:t}}},"5e96":function(e){e.exports=JSON.parse('{"a":"https://res.wx.qq.com/mpres/zh_CN/htmledition/comm_htmledition/images/pic/common/pic_blank.gif"}')},"605d":function(e,t,n){var r=n("c6b6"),o=n("da84");e.exports="process"==r(o.process)},6547:function(e,t,n){var r=n("a691"),o=n("1d80"),i=function(e){return function(t,n){var i,s,a=String(o(t)),c=r(n),u=a.length;return c<0||c>=u?e?"":void 0:(i=a.charCodeAt(c),i<55296||i>56319||c+1===u||(s=a.charCodeAt(c+1))<56320||s>57343?e?a.charAt(c):i:e?a.slice(c,c+2):s-56320+(i-55296<<10)+65536)}};e.exports={codeAt:i(!1),charAt:i(!0)}},"65f0":function(e,t,n){var r=n("861d"),o=n("e8b5"),i=n("b622"),s=i("species");e.exports=function(e,t){var n;return o(e)&&(n=e.constructor,"function"!=typeof n||n!==Array&&!o(n.prototype)?r(n)&&(n=n[s],null===n&&(n=void 0)):n=void 0),new(void 0===n?Array:n)(0===t?0:t)}},"69f3":function(e,t,n){var r,o,i,s=n("7f9a"),a=n("da84"),c=n("861d"),u=n("9112"),p=n("5135"),f=n("c6cd"),l=n("f772"),h=n("d012"),d=a.WeakMap,y=function(e){return i(e)?o(e):r(e,{})},x=function(e){return function(t){var n;if(!c(t)||(n=o(t)).type!==e)throw TypeError("Incompatible receiver, "+e+" required");return n}};if(s){var m=f.state||(f.state=new d),g=m.get,w=m.has,_=m.set;r=function(e,t){return t.facade=e,_.call(m,e,t),t},o=function(e){return g.call(m,e)||{}},i=function(e){return w.call(m,e)}}else{var v=l("state");h[v]=!0,r=function(e,t){return t.facade=e,u(e,v,t),t},o=function(e){return p(e,v)?e[v]:{}},i=function(e){return p(e,v)}}e.exports={set:r,get:o,has:i,enforce:y,getterFor:x}},"6eeb":function(e,t,n){var r=n("da84"),o=n("9112"),i=n("5135"),s=n("ce4e"),a=n("8925"),c=n("69f3"),u=c.get,p=c.enforce,f=String(String).split("String");(e.exports=function(e,t,n,a){var c,u=!!a&&!!a.unsafe,l=!!a&&!!a.enumerable,h=!!a&&!!a.noTargetGet;"function"==typeof n&&("string"!=typeof t||i(n,"name")||o(n,"name",t),c=p(n),c.source||(c.source=f.join("string"==typeof t?t:""))),e!==r?(u?!h&&e[t]&&(l=!0):delete e[t],l?e[t]=n:o(e,t,n)):l?e[t]=n:s(t,n)})(Function.prototype,"toString",(function(){return"function"==typeof this&&u(this).source||a(this)}))},"6f53":function(e,t,n){var r=n("83ab"),o=n("df75"),i=n("fc6a"),s=n("d1e7").f,a=function(e){return function(t){var n,a=i(t),c=o(a),u=c.length,p=0,f=[];while(u>p)n=c[p++],r&&!s.call(a,n)||f.push(e?[n,a[n]]:a[n]);return f}};e.exports={entries:a(!0),values:a(!1)}},7156:function(e,t,n){var r=n("861d"),o=n("d2bb");e.exports=function(e,t,n){var i,s;return o&&"function"==typeof(i=t.constructor)&&i!==n&&r(s=i.prototype)&&s!==n.prototype&&o(e,s),e}},7418:function(e,t){t.f=Object.getOwnPropertySymbols},"746f":function(e,t,n){var r=n("428f"),o=n("5135"),i=n("e538"),s=n("9bf2").f;e.exports=function(e){var t=r.Symbol||(r.Symbol={});o(t,e)||s(t,e,{value:i.f(e)})}},7839:function(e,t){e.exports=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"]},"7b0b":function(e,t,n){var r=n("1d80");e.exports=function(e){return Object(r(e))}},"7c73":function(e,t,n){var r,o=n("825a"),i=n("37e8"),s=n("7839"),a=n("d012"),c=n("1be4"),u=n("cc12"),p=n("f772"),f=">",l="<",h="prototype",d="script",y=p("IE_PROTO"),x=function(){},m=function(e){return l+d+f+e+l+"/"+d+f},g=function(e){e.write(m("")),e.close();var t=e.parentWindow.Object;return e=null,t},w=function(){var e,t=u("iframe"),n="java"+d+":";return t.style.display="none",c.appendChild(t),t.src=String(n),e=t.contentWindow.document,e.open(),e.write(m("document.F=Object")),e.close(),e.F},_=function(){try{r=document.domain&&new ActiveXObject("htmlfile")}catch(t){}_=r?g(r):w();var e=s.length;while(e--)delete _[h][s[e]];return _()};a[y]=!0,e.exports=Object.create||function(e,t){var n;return null!==e?(x[h]=o(e),n=new x,x[h]=null,n[y]=e):n=_(),void 0===t?n:i(n,t)}},"7db0":function(e,t,n){"use strict";var r=n("23e7"),o=n("b727").find,i=n("44d2"),s="find",a=!0;s in[]&&Array(1)[s]((function(){a=!1})),r({target:"Array",proto:!0,forced:a},{find:function(e){return o(this,e,arguments.length>1?arguments[1]:void 0)}}),i(s)},"7dd0":function(e,t,n){"use strict";var r=n("23e7"),o=n("9ed3"),i=n("e163"),s=n("d2bb"),a=n("d44e"),c=n("9112"),u=n("6eeb"),p=n("b622"),f=n("c430"),l=n("3f8c"),h=n("ae93"),d=h.IteratorPrototype,y=h.BUGGY_SAFARI_ITERATORS,x=p("iterator"),m="keys",g="values",w="entries",_=function(){return this};e.exports=function(e,t,n,p,h,v,b){o(n,t,p);var E,j,k,S=function(e){if(e===h&&q)return q;if(!y&&e in T)return T[e];switch(e){case m:return function(){return new n(this,e)};case g:return function(){return new n(this,e)};case w:return function(){return new n(this,e)}}return function(){return new n(this)}},O=t+" Iterator",P=!1,T=e.prototype,D=T[x]||T["@@iterator"]||h&&T[h],q=!y&&D||S(h),A="Array"==t&&T.entries||D;if(A&&(E=i(A.call(new e)),d!==Object.prototype&&E.next&&(f||i(E)===d||(s?s(E,d):"function"!=typeof E[x]&&c(E,x,_)),a(E,O,!0,!0),f&&(l[O]=_))),h==g&&D&&D.name!==g&&(P=!0,q=function(){return D.call(this)}),f&&!b||T[x]===q||c(T,x,q),l[t]=q,h)if(j={values:S(g),keys:v?q:S(m),entries:S(w)},b)for(k in j)(y||P||!(k in T))&&u(T,k,j[k]);else r({target:t,proto:!0,forced:y||P},j);return j}},"7f9a":function(e,t,n){var r=n("da84"),o=n("8925"),i=r.WeakMap;e.exports="function"===typeof i&&/native code/.test(o(i))},"825a":function(e,t,n){var r=n("861d");e.exports=function(e){if(!r(e))throw TypeError(String(e)+" is not an object");return e}},"83ab":function(e,t,n){var r=n("d039");e.exports=!r((function(){return 7!=Object.defineProperty({},1,{get:function(){return 7}})[1]}))},8418:function(e,t,n){"use strict";var r=n("c04e"),o=n("9bf2"),i=n("5c6c");e.exports=function(e,t,n){var s=r(t);s in e?o.f(e,s,i(0,n)):e[s]=n}},"861d":function(e,t){e.exports=function(e){return"object"===typeof e?null!==e:"function"===typeof e}},8875:function(e,t,n){var r,o,i;(function(n,s){o=[],r=s,i="function"===typeof r?r.apply(t,o):r,void 0===i||(e.exports=i)})("undefined"!==typeof self&&self,(function(){function e(){var t=Object.getOwnPropertyDescriptor(document,"currentScript");if(!t&&"currentScript"in document&&document.currentScript)return document.currentScript;if(t&&t.get!==e&&document.currentScript)return document.currentScript;try{throw new Error}catch(h){var n,r,o,i=/.*at [^(]*\((.*):(.+):(.+)\)$/gi,s=/@([^@]*):(\d+):(\d+)\s*$/gi,a=i.exec(h.stack)||s.exec(h.stack),c=a&&a[1]||!1,u=a&&a[2]||!1,p=document.location.href.replace(document.location.hash,""),f=document.getElementsByTagName("script");c===p&&(n=document.documentElement.outerHTML,r=new RegExp("(?:[^\\n]+?\\n){0,"+(u-2)+"}[^<]*<script>([\\d\\D]*?)<\\/script>[\\d\\D]*","i"),o=n.replace(r,"$1").trim());for(var l=0;l<f.length;l++){if("interactive"===f[l].readyState)return f[l];if(f[l].src===c)return f[l];if(c===p&&f[l].innerHTML&&f[l].innerHTML.trim()===o)return f[l]}return null}}return e}))},8925:function(e,t,n){var r=n("c6cd"),o=Function.toString;"function"!=typeof r.inspectSource&&(r.inspectSource=function(e){return o.call(e)}),e.exports=r.inspectSource},"8aa5":function(e,t,n){"use strict";var r=n("6547").charAt;e.exports=function(e,t,n){return t+(n?r(e,t).length:1)}},"8c94":function(e){e.exports=JSON.parse('[{"key":"/::)","old":"/微笑","cn":"[微笑]","tw":"[微笑]","en":"[Smile]","th":"[ยิ้ม]","path":"./assets/Expression/Expression_1@2x.png","style":"we-emoji__Smile"},{"key":"/::~","old":"/撇嘴","cn":"[撇嘴]","tw":"[撇嘴]","en":"[Grimace]","th":"[หน้าบูด]","path":"./assets/Expression/Expression_2@2x.png","style":"we-emoji__Grimace"},{"key":"/::B","old":"/色","cn":"[色]","tw":"[色]","en":"[Drool]","th":"[น้ำลายไหล]","path":"./assets/Expression/Expression_3@2x.png","style":"we-emoji__Drool"},{"key":"/::|","old":"/发呆","cn":"[发呆]","tw":"[發呆]","en":"[Scowl]","th":"[หน้าบึ้ง]","path":"./assets/Expression/Expression_4@2x.png","style":"we-emoji__Scowl"},{"key":"/:8-)","old":"/得意","cn":"[得意]","tw":"[得意]","en":"[CoolGuy]","th":"[สบาย]","path":"./assets/Expression/Expression_5@2x.png","style":"we-emoji__CoolGuy"},{"key":"/::<","old":"/流泪","cn":"[流泪]","tw":"[流淚]","en":"[Sob]","th":"[ร้องไห้โฮ]","path":"./assets/Expression/Expression_6@2x.png","style":"we-emoji__Sob"},{"key":"/::$","old":"/害羞","cn":"[害羞]","tw":"[害羞]","en":"[Shy]","th":"[อาย]","path":"./assets/Expression/Expression_7@2x.png","style":"we-emoji__Shy"},{"key":"/::X","old":"/闭嘴","cn":"[闭嘴]","tw":"[閉嘴]","en":"[Silent]","th":"[ห้ามพูด]","path":"./assets/Expression/Expression_8@2x.png","style":"we-emoji__Silent"},{"key":"/::Z","old":"/睡","cn":"[睡]","tw":"[睡]","en":"[Sleep]","th":"[หลับ]","path":"./assets/Expression/Expression_9@2x.png","style":"we-emoji__Sleep"},{"key":"/::\'(","old":"/大哭","cn":"[大哭]","tw":"[大哭]","en":"[Cry]","th":"[ร้องไห้]","path":"./assets/Expression/Expression_10@2x.png","style":"we-emoji__Cry"},{"key":"/::-|","old":"/尴尬","cn":"[尴尬]","tw":"[尷尬]","en":"[Awkward]","th":"[ลำบากใจ]","path":"./assets/Expression/Expression_11@2x.png","style":"we-emoji__Awkward"},{"key":"/::@","old":"/发怒","cn":"[发怒]","tw":"[發怒]","en":"[Angry]","th":"[โกรธสุด]","path":"./assets/Expression/Expression_12@2x.png","style":"we-emoji__Angry"},{"key":"/::P","old":"/调皮","qq":"[吐舌]","cn":"[调皮]","tw":"[調皮]","en":"[Tongue]","th":"[ขยิบตา]","emoji":"😝","path":"./assets/Expression/Expression_13@2x.png","style":"we-emoji__Tongue"},{"key":"/::D","old":"/呲牙","cn":"[呲牙]","tw":"[呲牙]","en":"[Grin]","th":"[ยิ้มกว้าง]","path":"./assets/Expression/Expression_14@2x.png","style":"we-emoji__Grin"},{"key":"/::O","old":"/惊讶","cn":"[惊讶]","tw":"[驚訝]","en":"[Surprise]","th":"[ประหลาดใจ]","path":"./assets/Expression/Expression_15@2x.png","style":"we-emoji__Surprise"},{"key":"/::(","old":"/难过","cn":"[难过]","tw":"[難過]","en":"[Frown]","th":"[เสียใจ]","path":"./assets/Expression/Expression_16@2x.png","style":"we-emoji__Frown"},{"key":"/::+","old":"/酷","cn":"[酷]","tw":"[酷]","en":"[Ruthless]","th":"[เจ๋ง]","path":"./assets/Expression/Expression_17@2x.png","style":"we-emoji__Ruthless"},{"key":"/:--b","old":"/冷汗","cn":"[囧]","tw":"[囧]","en":"[Blush]","th":"[Blush]","path":"./assets/Expression/Expression_18@2x.png","style":"we-emoji__Blush"},{"key":"/::Q","old":"/抓狂","cn":"[抓狂]","tw":"[抓狂]","en":"[Scream]","th":"[กรีดร้อง]","path":"./assets/Expression/Expression_19@2x.png","style":"we-emoji__Scream"},{"key":"/::T","old":"/吐","cn":"[吐]","tw":"[吐]","en":"[Puke]","th":"[อาเจียน]","path":"./assets/Expression/Expression_20@2x.png","style":"we-emoji__Puke"},{"key":"/:,@P","old":"/偷笑","cn":"[偷笑]","tw":"[偷笑]","en":"[Chuckle]","th":"[หัวเราะหึๆ]","path":"./assets/Expression/Expression_21@2x.png","style":"we-emoji__Chuckle"},{"key":"/:,@-D","old":"/可爱","cn":"[愉快]","tw":"[愉快]","en":"[Joyful]","th":"[พอใจ]","path":"./assets/Expression/Expression_22@2x.png","style":"we-emoji__Joyful"},{"key":"/::d","old":"/白眼","cn":"[白眼]","tw":"[白眼]","en":"[Slight]","th":"[สงสัย]","path":"./assets/Expression/Expression_23@2x.png","style":"we-emoji__Slight"},{"key":"/:,@o","old":"/傲慢","cn":"[傲慢]","tw":"[傲慢]","en":"[Smug]","th":"[หยิ่ง]","path":"./assets/Expression/Expression_24@2x.png","style":"we-emoji__Smug"},{"key":"/::g","old":"/饥饿","cn":"[饥饿]","tw":"[饑餓]","en":"[Hungry]","th":"[หิว]","path":"./assets/Expression/Expression_25@2x.png","style":"we-emoji__Hungry"},{"key":"/:|-)","old":"/困","cn":"[困]","tw":"[累]","en":"[Drowsy]","th":"[ง่วงนอน]","path":"./assets/Expression/Expression_26@2x.png","style":"we-emoji__Drowsy"},{"key":"/::!","old":"/惊恐","cn":"[惊恐]","tw":"[驚恐]","en":"[Panic]","th":"[ตกใจกลัว]","path":"./assets/Expression/Expression_27@2x.png","style":"we-emoji__Panic"},{"key":"/::L","old":"/流汗","cn":"[流汗]","tw":"[流汗]","en":"[Sweat]","th":"[เหงื่อตก]","path":"./assets/Expression/Expression_28@2x.png","style":"we-emoji__Sweat"},{"key":"/::>","old":"/憨笑","cn":"[憨笑]","tw":"[大笑]","en":"[Laugh]","th":"[หัวเราะ]","path":"./assets/Expression/Expression_29@2x.png","style":"we-emoji__Laugh"},{"key":"/::,@","old":"/大兵","cn":"[悠闲]","tw":"[悠閑]","en":"[Commando]","th":"[ทหาร]","path":"./assets/Expression/Expression_30@2x.png","style":"we-emoji__Commando"},{"key":"/:,@f","old":"/奋斗","cn":"[奋斗]","tw":"[奮鬥]","en":"[Determined]","th":"[มุ่งมั่น]","path":"./assets/Expression/Expression_31@2x.png","style":"we-emoji__Determined"},{"key":"/::-S","old":"/咒骂","cn":"[咒骂]","tw":"[咒罵]","en":"[Scold]","th":"[ด่าว่าา]","path":"./assets/Expression/Expression_32@2x.png","style":"we-emoji__Scold"},{"key":"/:?","old":"/疑问","cn":"[疑问]","tw":"[疑問]","en":"[Shocked]","th":"[สับสน]","path":"./assets/Expression/Expression_33@2x.png","style":"we-emoji__Shocked"},{"key":"/:,@x","old":"/嘘","cn":"[嘘]","tw":"[噓]","en":"[Shhh]","th":"[จุ๊ๆ]","path":"./assets/Expression/Expression_34@2x.png","style":"we-emoji__Shhh"},{"key":"/:,@@","old":"/晕","cn":"[晕]","tw":"[暈]","en":"[Dizzy]","th":"[เวียนหัว]","path":"./assets/Expression/Expression_35@2x.png","style":"we-emoji__Dizzy"},{"key":"/::8","old":"/折磨","cn":"[疯了]","tw":"[瘋了]","en":"[Tormented]","th":"[ท้อแท้]","path":"./assets/Expression/Expression_36@2x.png","style":"we-emoji__Tormented"},{"key":"/:,@!","old":"/衰","cn":"[衰]","tw":"[衰]","en":"[Toasted]","th":"[ชั่วร้าย]","path":"./assets/Expression/Expression_37@2x.png","style":"we-emoji__Toasted"},{"key":"/:!!!","old":"/骷髅","cn":"[骷髅]","tw":"[骷髏頭]","en":"[Skull]","th":"[หัวกะโหลก]","path":"./assets/Expression/Expression_38@2x.png","style":"we-emoji__Skull"},{"key":"/:xx","old":"/敲打","cn":"[敲打]","tw":"[敲打]","en":"[Hammer]","th":"[ค้อนทุบ]","path":"./assets/Expression/Expression_39@2x.png","style":"we-emoji__Hammer"},{"key":"/:bye","old":"/再见","cn":"[再见]","tw":"[再見]","en":"[Wave]","th":"[บายๆ]","path":"./assets/Expression/Expression_40@2x.png","style":"we-emoji__Wave"},{"key":"/:wipe","old":"/擦汗","cn":"[擦汗]","tw":"[擦汗]","en":"[Speechless]","th":"[เช็ดเหงื่อ]","path":"./assets/Expression/Expression_41@2x.png","style":"we-emoji__Speechless"},{"key":"/:dig","old":"/抠鼻","cn":"[抠鼻]","tw":"[摳鼻]","en":"[NosePick]","th":"[แคะจมูก]","path":"./assets/Expression/Expression_42@2x.png","style":"we-emoji__NosePick"},{"key":"/:handclap","old":"/鼓掌","cn":"[鼓掌]","tw":"[鼓掌]","en":"[Clap]","th":"[ตบมือ]","path":"./assets/Expression/Expression_43@2x.png","style":"we-emoji__Clap"},{"key":"/:&-(","old":"/糗大了","cn":"[糗大了]","tw":"[羞辱]","en":"[Shame]","th":"[อับอาย]","path":"./assets/Expression/Expression_44@2x.png","style":"we-emoji__Shame"},{"key":"/:B-)","old":"/坏笑","cn":"[坏笑]","tw":"[壞笑]","en":"[Trick]","th":"[กลโกง]","path":"./assets/Expression/Expression_45@2x.png","style":"we-emoji__Trick"},{"key":"/:<@","old":"/左哼哼","cn":"[左哼哼]","tw":"[左哼哼]","en":"[Bah！L]","th":"[เชิดซ้าย]","path":"./assets/Expression/Expression_46@2x.png","style":"we-emoji__BahL"},{"key":"/:@>","old":"/右哼哼","cn":"[右哼哼]","tw":"[右哼哼]","en":"[Bah！R]","th":"[เชิดขวา]","path":"./assets/Expression/Expression_47@2x.png","style":"we-emoji__BahR"},{"key":"/::-O","old":"/哈欠","cn":"[哈欠]","tw":"[哈欠]","en":"[Yawn]","th":"[หาว]","path":"./assets/Expression/Expression_48@2x.png","style":"we-emoji__Yawn"},{"key":"/:>-|","old":"/鄙视","cn":"[鄙视]","tw":"[鄙視]","en":"[Pooh-pooh]","th":"[ดูถูก]","path":"./assets/Expression/Expression_49@2x.png","style":"we-emoji__Pooh-pooh"},{"key":"/:P-(","old":"/委屈","cn":"[委屈]","tw":"[委屈]","en":"[Shrunken]","th":"[ข้องใจ]","path":"./assets/Expression/Expression_50@2x.png","style":"we-emoji__Shrunken"},{"key":"/::\'|","old":"/快哭了","cn":"[快哭了]","tw":"[快哭了]","en":"[TearingUp]","th":"[เกือบร้องไห้]","path":"./assets/Expression/Expression_51@2x.png","style":"we-emoji__TearingUp"},{"key":"/:X-)","old":"/阴险","cn":"[阴险]","tw":"[陰險]","en":"[Sly]","th":"[ขี้โกง]","path":"./assets/Expression/Expression_52@2x.png","style":"we-emoji__Sly"},{"key":"/::*","old":"/亲亲","cn":"[亲亲]","tw":"[親親]","en":"[Kiss]","th":"[จุ๊บ]","path":"./assets/Expression/Expression_53@2x.png","style":"we-emoji__Kiss"},{"key":"/:@x","old":"/吓","cn":"[吓]","tw":"[嚇]","en":"[Wrath]","th":"[ห๊า]","path":"./assets/Expression/Expression_54@2x.png","style":"we-emoji__Wrath"},{"key":"/:8*","old":"/可怜","cn":"[可怜]","tw":"[可憐]","en":"[Whimper]","th":"[น่าสงสาร]","path":"./assets/Expression/Expression_55@2x.png","style":"we-emoji__Whimper"},{"key":"/:pd","old":"/菜刀","cn":"[菜刀]","tw":"[菜刀]","en":"[Cleaver]","th":"[มีด]","path":"./assets/Expression/Expression_56@2x.png","style":"we-emoji__Cleaver"},{"key":"/:<W>","old":"/西瓜","cn":"[西瓜]","tw":"[西瓜]","en":"[Watermelon]","th":"[แตงโม]","path":"./assets/Expression/Expression_57@2x.png","style":"we-emoji__Watermelon"},{"key":"/:beer","old":"/啤酒","cn":"[啤酒]","tw":"[啤酒]","en":"[Beer]","th":"[เบียร์]","path":"./assets/Expression/Expression_58@2x.png","style":"we-emoji__Beer"},{"key":"/:basketb","old":"/篮球","cn":"[篮球]","tw":"[籃球]","en":"[Basketball]","th":"[บาสเกตบอล]","path":"./assets/Expression/Expression_59@2x.png","style":"we-emoji__Basketball"},{"key":"/:oo","old":"/乒乓","cn":"[乒乓]","tw":"[乒乓]","en":"[PingPong]","th":"[ปิงปอง]","path":"./assets/Expression/Expression_60@2x.png","style":"we-emoji__PingPong"},{"key":"/:coffee","old":"/咖啡","cn":"[咖啡]","tw":"[咖啡]","en":"[Coffee]","th":"[กาแฟ]","path":"./assets/Expression/Expression_61@2x.png","style":"we-emoji__Coffee"},{"key":"/:eat","old":"/饭","cn":"[饭]","tw":"[飯]","en":"[Rice]","th":"[ข้าว]","path":"./assets/Expression/Expression_62@2x.png","style":"we-emoji__Rice"},{"key":"/:pig","old":"/猪头","cn":"[猪头]","tw":"[豬頭]","en":"[Pig]","th":"[หมู]","path":"./assets/Expression/Expression_63@2x.png","style":"we-emoji__Pig"},{"key":"/:rose","old":"/玫瑰","cn":"[玫瑰]","tw":"[玫瑰]","en":"[Rose]","th":"[กุหลาบ]","path":"./assets/Expression/Expression_64@2x.png","style":"we-emoji__Rose"},{"key":"/:fade","old":"/凋谢","cn":"[凋谢]","tw":"[枯萎]","en":"[Wilt]","th":"[ร่วงโรย]","path":"./assets/Expression/Expression_65@2x.png","style":"we-emoji__Wilt"},{"key":"/:showlove","old":"/示爱","cn":"[嘴唇]","tw":"[嘴唇]","en":"[Lips]","th":"[ริมฝีปาก]","path":"./assets/Expression/Expression_66@2x.png","style":"we-emoji__Lips"},{"key":"/:heart","old":"/爱心","cn":"[爱心]","tw":"[愛心]","en":"[Heart]","th":"[หัวใจ]","path":"./assets/Expression/Expression_67@2x.png","style":"we-emoji__Heart"},{"key":"/:break","old":"/心碎","cn":"[心碎]","tw":"[心碎]","en":"[BrokenHeart]","th":"[ใจสลาย]","path":"./assets/Expression/Expression_68@2x.png","style":"we-emoji__BrokenHeart"},{"key":"/:cake","old":"/蛋糕","cn":"[蛋糕]","tw":"[蛋糕]","en":"[Cake]","th":"[เค้ก]","path":"./assets/Expression/Expression_69@2x.png","style":"we-emoji__Cake"},{"key":"/:li","old":"/闪电","cn":"[闪电]","tw":"[閃電]","en":"[Lightning]","th":"[ฟ้าผ่า]","path":"./assets/Expression/Expression_70@2x.png","style":"we-emoji__Lightning"},{"key":"/:bome","old":"/炸弹","cn":"[炸弹]","tw":"[炸彈]","en":"[Bomb]","th":"[ระเบิด]","path":"./assets/Expression/Expression_71@2x.png","style":"we-emoji__Bomb"},{"key":"/:kn","old":"/刀","cn":"[刀]","tw":"[刀]","en":"[Dagger]","th":"[ดาบ]","path":"./assets/Expression/Expression_72@2x.png","style":"we-emoji__Dagger"},{"key":"/:footb","old":"/足球","cn":"[足球]","tw":"[足球]","en":"[Soccer]","th":"[ฟุตบอล]","path":"./assets/Expression/Expression_73@2x.png","style":"we-emoji__Soccer"},{"key":"/:ladybug","old":"/瓢虫","cn":"[瓢虫]","tw":"[甲蟲]","en":"[Ladybug]","th":"[เต่าทอง]","path":"./assets/Expression/Expression_74@2x.png","style":"we-emoji__Ladybug"},{"key":"/:shit","old":"/便便","cn":"[便便]","tw":"[便便]","en":"[Poop]","th":"[อุจจาระ]","path":"./assets/Expression/Expression_75@2x.png","style":"we-emoji__Poop"},{"key":"/:moon","old":"/月亮","cn":"[月亮]","tw":"[月亮]","en":"[Moon]","th":"[พระจันทร์]","path":"./assets/Expression/Expression_76@2x.png","style":"we-emoji__Moon"},{"key":"/:sun","old":"/太阳","cn":"[太阳]","tw":"[太陽]","en":"[Sun]","th":"[พระอาทิตย์]","path":"./assets/Expression/Expression_77@2x.png","style":"we-emoji__Sun"},{"key":"/:gift","old":"/礼物","cn":"[礼物]","tw":"[禮物]","en":"[礼物]","th":"[Gift]","emoji":"🎁","path":"./assets/Expression/Expression_78@2x.png","style":"we-emoji__Gift"},{"key":"/:hug","old":"/拥抱","cn":"[拥抱]","tw":"[擁抱]","en":"[Hug]","th":"[กอด]","path":"./assets/Expression/Expression_79@2x.png","style":"we-emoji__Hug"},{"key":"/:strong","old":"/强","cn":"[强]","tw":"[強]","en":"[ThumbsUp]","th":"[ยอดเยี่ยม]","path":"./assets/Expression/Expression_80@2x.png","style":"we-emoji__ThumbsUp"},{"key":"/:weak","old":"/弱","cn":"[弱]","tw":"[弱]","en":"[ThumbsDown]","th":"[ยอดแย่]","path":"./assets/Expression/Expression_81@2x.png","style":"we-emoji__ThumbsDown"},{"key":"/:share","old":"/握手","cn":"[握手]","tw":"[握手]","en":"[Shake]","th":"[จับมือ]","path":"./assets/Expression/Expression_82@2x.png","style":"we-emoji__Shake"},{"key":"/:v","old":"/胜利","cn":"[胜利]","tw":"[勝利]","en":"[Peace]","th":"[สู้ตาย]","path":"./assets/Expression/Expression_83@2x.png","style":"we-emoji__Peace"},{"key":"/:@)","old":"/抱拳","cn":"[抱拳]","tw":"[抱拳]","en":"[Fight]","th":"[คารวะ]","path":"./assets/Expression/Expression_84@2x.png","style":"we-emoji__Fight"},{"key":"/:jj","old":"/勾引","cn":"[勾引]","tw":"[勾引]","en":"[Beckon]","th":"[เข้ามา]","path":"./assets/Expression/Expression_85@2x.png","style":"we-emoji__Beckon"},{"key":"/:@@","old":"/拳头","cn":"[拳头]","tw":"[拳頭]","en":"[Fist]","th":"[กำหมัด]","path":"./assets/Expression/Expression_86@2x.png","style":"we-emoji__Fist"},{"key":"/:bad","old":"/差劲","cn":"[差劲]","tw":"[差勁]","en":"[Pinky]","th":"[ดีกัน]","path":"./assets/Expression/Expression_87@2x.png","style":"we-emoji__Pinky"},{"key":"/:lvu","old":"/爱你","cn":"[爱你]","tw":"[愛你]","en":"[RockOn]","th":"[ฉันรักคุณ]","path":"./assets/Expression/Expression_88@2x.png","style":"we-emoji__RockOn"},{"key":"/:no","old":"/NO","cn":"[NO]","tw":"[NO]","en":"[Nuh-uh]","th":"[ไม่]","path":"./assets/Expression/Expression_89@2x.png","style":"we-emoji__Nuh-uh"},{"key":"/:ok","old":"/OK","cn":"[OK]","tw":"[OK]","en":"[OK]","th":"[ตกลง]","path":"./assets/Expression/Expression_90@2x.png","style":"we-emoji__OK"},{"key":"/:love","old":"/爱情","cn":"[爱情]","tw":"[愛情]","en":"[InLove]","th":"[รักกัน]","path":"./assets/Expression/Expression_91@2x.png","style":"we-emoji__InLove"},{"key":"/:<L>","old":"/飞吻","cn":"[飞吻]","tw":"[飛吻]","en":"[Blowkiss]","th":"[มีรัก]","path":"./assets/Expression/Expression_92@2x.png","style":"we-emoji__Blowkiss"},{"key":"/:jump","old":"/跳跳","cn":"[跳跳]","tw":"[跳跳]","en":"[Waddle]","th":"[กระโดด]","path":"./assets/Expression/Expression_93@2x.png","style":"we-emoji__Waddle"},{"key":"/:shake","old":"/发抖","cn":"[发抖]","tw":"[發抖]","en":"[Tremble]","th":"[เขย่า]","path":"./assets/Expression/Expression_94@2x.png","style":"we-emoji__Tremble"},{"key":"/:<O>","old":"/怄火","cn":"[怄火]","tw":"[噴火]","en":"[Aaagh!]","th":"[อ้ากส์!]","path":"./assets/Expression/Expression_95@2x.png","style":"we-emoji__Aaagh"},{"key":"/:circle","old":"/转圈","cn":"[转圈]","tw":"[轉圈]","en":"[Twirl]","th":"[หมุนตัว]","path":"./assets/Expression/Expression_96@2x.png","style":"we-emoji__Twirl"},{"key":"/:kotow","old":"/磕头","cn":"[磕头]","tw":"[磕頭]","en":"[Kotow]","th":"[คำนับ]","path":"./assets/Expression/Expression_97@2x.png","style":"we-emoji__Kotow"},{"key":"/:turn","old":"/回头","cn":"[回头]","tw":"[回頭]","en":"[Dramatic]","th":"[เหลียวหลัง]","path":"./assets/Expression/Expression_98@2x.png","style":"we-emoji__Dramatic"},{"key":"/:skip","old":"/跳绳","cn":"[跳绳]","tw":"[跳繩]","en":"[JumpRope]","th":"[กระโดด]","path":"./assets/Expression/Expression_99@2x.png","style":"we-emoji__JumpRope"},{"key":"/:oY","old":"/挥手","cn":"[投降]","tw":"[投降]","en":"[Surrender]","th":"[ยอมแพ้]","path":"./assets/Expression/Expression_100@2x.png","style":"we-emoji__Surrender"},{"key":"/:#-0","old":"/激动","cn":"[激动]","tw":"[激動]","en":"[Hooray]","th":"[ไชโย]","path":"./assets/Expression/Expression_101@2x.png","style":"we-emoji__Hooray"},{"key":"/:hiphot","old":"/街舞","cn":"[乱舞]","tw":"[亂舞]","en":"[Meditate]","th":"[เย้เย้]","path":"./assets/Expression/Expression_102@2x.png","style":"we-emoji__Meditate"},{"key":"/:kiss","old":"/献吻","cn":"[献吻]","tw":"[獻吻]","en":"[Smooch]","th":"[จูบ]","path":"./assets/Expression/Expression_103@2x.png","style":"we-emoji__Smooch"},{"key":"/:<&","old":"/左太极","cn":"[左太极]","tw":"[左太極]","en":"[TaiChi L]","th":"[หญิงต่อสู้]","path":"./assets/Expression/Expression_104@2x.png","style":"we-emoji__TaiChiL"},{"key":"/:&\\"","old":"/右太极","cn":"[右太极]","tw":"[右太極]","en":"[TaiChi R]","th":"[ชายต่อสู้]","path":"./assets/Expression/Expression_105@2x.png","style":"we-emoji__TaiChiR"},{"key":"[Smirk]","cn":"[奸笑]","qq":"[奸笑]","en":"[Smirk]","tw":"[奸笑]","th":"[Smirk]","path":"./assets/newemoji/2_02.png","style":"we-emoji__Smirk"},{"key":"[Hey]","cn":"[嘿哈]","qq":"[嘿哈]","en":"[Hey]","tw":"[吼嘿]","th":"[Hey]","path":"./assets/newemoji/2_04.png","style":"we-emoji__Hey"},{"key":"[Facepalm]","cn":"[捂脸]","qq":"[捂脸]","en":"[Facepalm]","tw":"[掩面]","th":"[Facepalm]","path":"./assets/newemoji/2_05.png","style":"we-emoji__Facepalm"},{"key":"[Smart]","cn":"[机智]","qq":"[机智]","en":"[Smart]","tw":"[機智]","th":"[Smart]","path":"./assets/newemoji/2_06.png","style":"we-emoji__Smart"},{"key":"[Tea]","cn":"[茶]","qq":"[茶]","en":"[Tea]","tw":"[茶]","th":"[Tea]","path":"./assets/newemoji/2_07.png","style":"we-emoji__Tea"},{"key":"[Packet]","cn":"[红包]","qq":"[红包]","en":"[Packet]","tw":"[Packet]","th":"[Packet]","path":"./assets/newemoji/2_09.png","style":"we-emoji__Packet"},{"key":"[Candle]","cn":"[蜡烛]","qq":"[蜡烛]","en":"[Candle]","tw":"[蠟燭]","th":"[Candle]","path":"./assets/newemoji/2_10.png","style":"we-emoji__Candle"},{"key":"[Yeah!]","cn":"[耶]","qq":"[耶]","en":"[Yeah!]","tw":"[歐耶]","th":"[Yeah!]","path":"./assets/newemoji/2_11.png","style":"we-emoji__Yeah"},{"key":"[Concerned]","cn":"[皱眉]","qq":"[皱眉]","en":"[Concerned]","tw":"[皺眉]","th":"[Concerned]","path":"./assets/newemoji/2_12.png","style":"we-emoji__Concerned"},{"key":"[Salute]","cn":"[抱拳]","qq":"[抱拳]","en":"[Salute]","tw":"[抱拳]","th":"[Salute]","path":"./assets/newemoji/smiley_83b.png","style":"we-emoji__Salute"},{"key":"[Chick]","cn":"[鸡]","qq":"[鸡]","en":"[Chick]","tw":"[小雞]","th":"[Chick]","path":"./assets/newemoji/2_14.png","style":"we-emoji__Chick"},{"key":"[Blessing]","cn":"[福]","qq":"[福]","en":"[Blessing]","tw":"[福]","th":"[Blessing]","path":"./assets/newemoji/2_15.png","style":"we-emoji__Blessing"},{"key":"[Bye]","cn":"[再见]","qq":"[再见]","en":"[Bye]","tw":"[再見]","th":"[Bye]","path":"./assets/newemoji/smiley_39b.png","style":"we-emoji__Bye"},{"key":"[Rich]","cn":"[發]","qq":"[發]","en":"[Rich]","tw":"[發]","th":"[Rich]","path":"./assets/newemoji/2_16.png","style":"we-emoji__Rich"},{"key":"[Pup]","cn":"[小狗]","qq":"[小狗]","en":"[Pup]","tw":"[小狗]","th":"[Pup]","path":"./assets/newemoji/2_17.png","style":"we-emoji__Pup"},{"key":"[Onlooker]","cn":"[吃瓜]","qq":"[吃瓜]","en":"[Onlooker]","tw":"[吃西瓜]","th":"[Onlooker]","path":"./assets/newemoji/Watermelon.png","style":"we-emoji__Onlooker"},{"key":"[GoForIt]","cn":"[加油]","qq":"[加油]","en":"[GoForIt]","tw":"[加油]","th":"[GoForIt]","path":"./assets/newemoji/Addoil.png","style":"we-emoji__GoForIt"},{"key":"[Sweats]","cn":"[汗]","qq":"[汗]","en":"[Sweats]","tw":"[汗]","th":"[Sweats]","path":"./assets/newemoji/Sweat.png","style":"we-emoji__Sweats"},{"key":"[OMG]","cn":"[天啊]","qq":"[天啊]","en":"[OMG]","tw":"[天啊]","th":"[OMG]","path":"./assets/newemoji/Shocked.png","style":"we-emoji__OMG"},{"key":"[Emm]","cn":"[Emm]","qq":"[Emm]","en":"[Emm]","tw":"[一言難盡]","th":"[Emm]","path":"./assets/newemoji/Cold.png","style":"we-emoji__Emm"},{"key":"[Respect]","cn":"[社会社会]","qq":"[社会社会]","en":"[Respect]","tw":"[失敬失敬]","th":"[Respect]","path":"./assets/newemoji/Social.png","style":"we-emoji__Respect"},{"key":"[Doge]","cn":"[旺柴]","qq":"[旺柴]","en":"[Doge]","tw":"[旺柴]","th":"[Doge]","path":"./assets/newemoji/Yellowdog.png","style":"we-emoji__Doge"},{"key":"[NoProb]","cn":"[好的]","qq":"[好的]","en":"[NoProb]","tw":"[好的]","th":"[NoProb]","path":"./assets/newemoji/NoProb.png","style":"we-emoji__NoProb"},{"key":"[MyBad]","cn":"[打脸]","qq":"[打脸]","en":"[MyBad]","tw":"[打臉]","th":"[MyBad]","path":"./assets/newemoji/Slap.png","style":"we-emoji__MyBad"},{"key":"[Wow]","cn":"[哇]","qq":"[哇]","en":"[Wow]","tw":"[哇]","th":"[Wow]","path":"./assets/newemoji/Wow.png","style":"we-emoji__Wow"},{"key":"[KeepFighting]","cn":"[加油加油]","qq":"[加油加油]","en":"[KeepFighting]","tw":"[加油！]","th":"[KeepFighting]","path":"./assets/newemoji/KeepFighting.png","style":"we-emoji__KeepFighting"},{"key":"[Boring]","cn":"[翻白眼]","qq":"[翻白眼]","en":"[Boring]","tw":"[翻白眼]","th":"[Boring]","path":"./assets/newemoji/Boring.png","style":"we-emoji__Boring"},{"key":"[666]","cn":"[666]","qq":"[666]","en":"[Awesome]","tw":"[666]","th":"[Awesome]","path":"./assets/newemoji/666.png","style":"we-emoji__Awesome"},{"key":"[LetMeSee]","cn":"[让我看看]","qq":"[让我看看]","en":"[LetMeSee]","tw":"[讓我看看]","th":"[LetMeSee]","path":"./assets/newemoji/LetMeSee.png","style":"we-emoji__LetMeSee"},{"key":"[Sigh]","cn":"[叹气]","qq":"[叹气]","en":"[Sigh]","tw":"[嘆息]","th":"[Sigh]","path":"./assets/newemoji/Sigh.png","style":"we-emoji__Sigh"},{"key":"[Hurt]","cn":"[苦涩]","qq":"[苦涩]","en":"[Hurt]","tw":"[難受]","th":"[Hurt]","path":"./assets/newemoji/Hurt.png","style":"we-emoji__Hurt"},{"key":"[Broken]","cn":"[裂开]","qq":"[裂开]","en":"[Broken]","tw":"[崩潰]","th":"[Broken]","path":"./assets/newemoji/Broken.png","style":"we-emoji__Broken"},{"key":"[Flushed]","cn":"[脸红]","qq":"[脸红]","en":"[Flushed]","tw":"[臉紅]","th":"[Flushed]","emoji":"😳","path":"./assets/newemoji/Flushed.png","style":"we-emoji__Flushed"},{"key":"[Happy]","cn":"[笑脸]","qq":"[笑脸]","en":"[Happy]","tw":"[笑臉]","th":"[Happy]","emoji":"😄","path":"./assets/newemoji/Happy.png","style":"we-emoji__Happy"},{"key":"[Lol]","cn":"[破涕为笑]","qq":"[破涕为笑]","en":"[Lol]","tw":"[破涕為笑]","th":"[Lol]","emoji":"😂","path":"./assets/newemoji/Lol.png","style":"we-emoji__Lol"},{"key":"[Fireworks]","cn":"[烟花]","qq":"[烟花]","en":"[Fireworks]","tw":"[煙花]","th":"[Fireworks]","path":"./assets/newemoji/Fireworks.png","style":"we-emoji__Fireworks"},{"key":"[Firecracker]","cn":"[爆竹]","qq":"[爆竹]","en":"[Firecracker]","tw":"[爆竹]","th":"[Firecracker]","path":"./assets/newemoji/Firecracker.png","style":"we-emoji__Firecracker"},{"key":"[Party]","cn":"[庆祝]","qq":"[庆祝]","en":"[Party]","tw":"[慶祝]","th":"[Party]","emoji":"🎉","path":"./assets/newemoji/Party.png","style":"we-emoji__Party"},{"key":"[Terror]","cn":"[恐惧]","qq":"[恐惧]","en":"[Terror]","tw":"[恐懼]","th":"[Terror]","emoji":"😱","path":"./assets/newemoji/Terror.png","style":"we-emoji__Terror"},{"key":"[Duh]","cn":"[无语]","qq":"[无语]","en":"[Duh]","tw":"[無語]","th":"[Duh]","emoji":"😒","path":"./assets/newemoji/Duh.png","style":"we-emoji__Duh"},{"key":"[LetDown]","cn":"[失望]","qq":"[失望]","en":"[Let Down]","tw":"[失望]","th":"[Let Down]","emoji":"😔","path":"./assets/newemoji/LetDown.png","style":"we-emoji__LetDown"},{"key":"[Sick]","cn":"[生病]","qq":"[生病]","en":"[Sick]","tw":"[生病]","th":"[Sick]","emoji":"😷","path":"./assets/newemoji/Sick.png","style":"we-emoji__Sick"},{"key":"[Worship]","cn":"[合十]","qq":"[合十]","en":"[Worship]","tw":"[合十]","th":"[Worship]","emoji":"🙏","path":"./assets/newemoji/Worship.png","style":"we-emoji__Worship"}]')},"90e3":function(e,t){var n=0,r=Math.random();e.exports=function(e){return"Symbol("+String(void 0===e?"":e)+")_"+(++n+r).toString(36)}},9112:function(e,t,n){var r=n("83ab"),o=n("9bf2"),i=n("5c6c");e.exports=r?function(e,t,n){return o.f(e,t,i(1,n))}:function(e,t,n){return e[t]=n,e}},9263:function(e,t,n){"use strict";var r=n("ad6d"),o=n("9f7f"),i=RegExp.prototype.exec,s=String.prototype.replace,a=i,c=function(){var e=/a/,t=/b*/g;return i.call(e,"a"),i.call(t,"a"),0!==e.lastIndex||0!==t.lastIndex}(),u=o.UNSUPPORTED_Y||o.BROKEN_CARET,p=void 0!==/()??/.exec("")[1],f=c||p||u;f&&(a=function(e){var t,n,o,a,f=this,l=u&&f.sticky,h=r.call(f),d=f.source,y=0,x=e;return l&&(h=h.replace("y",""),-1===h.indexOf("g")&&(h+="g"),x=String(e).slice(f.lastIndex),f.lastIndex>0&&(!f.multiline||f.multiline&&"\n"!==e[f.lastIndex-1])&&(d="(?: "+d+")",x=" "+x,y++),n=new RegExp("^(?:"+d+")",h)),p&&(n=new RegExp("^"+d+"$(?!\\s)",h)),c&&(t=f.lastIndex),o=i.call(l?n:f,x),l?o?(o.input=o.input.slice(y),o[0]=o[0].slice(y),o.index=f.lastIndex,f.lastIndex+=o[0].length):f.lastIndex=0:c&&o&&(f.lastIndex=f.global?o.index+o[0].length:t),p&&o&&o.length>1&&s.call(o[0],n,(function(){for(a=1;a<arguments.length-2;a++)void 0===arguments[a]&&(o[a]=void 0)})),o}),e.exports=a},"94ca":function(e,t,n){var r=n("d039"),o=/#|\.prototype\./,i=function(e,t){var n=a[s(e)];return n==u||n!=c&&("function"==typeof t?r(t):!!t)},s=i.normalize=function(e){return String(e).replace(o,".").toLowerCase()},a=i.data={},c=i.NATIVE="N",u=i.POLYFILL="P";e.exports=i},9523:function(e,t){function n(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}e.exports=n,e.exports["default"]=e.exports,e.exports.__esModule=!0},"99af":function(e,t,n){"use strict";var r=n("23e7"),o=n("d039"),i=n("e8b5"),s=n("861d"),a=n("7b0b"),c=n("50c4"),u=n("8418"),p=n("65f0"),f=n("1dde"),l=n("b622"),h=n("2d00"),d=l("isConcatSpreadable"),y=9007199254740991,x="Maximum allowed index exceeded",m=h>=51||!o((function(){var e=[];return e[d]=!1,e.concat()[0]!==e})),g=f("concat"),w=function(e){if(!s(e))return!1;var t=e[d];return void 0!==t?!!t:i(e)},_=!m||!g;r({target:"Array",proto:!0,forced:_},{concat:function(e){var t,n,r,o,i,s=a(this),f=p(s,0),l=0;for(t=-1,r=arguments.length;t<r;t++)if(i=-1===t?s:arguments[t],w(i)){if(o=c(i.length),l+o>y)throw TypeError(x);for(n=0;n<o;n++,l++)n in i&&u(f,l,i[n])}else{if(l>=y)throw TypeError(x);u(f,l++,i)}return f.length=l,f}})},"9bdd":function(e,t,n){var r=n("825a"),o=n("2a62");e.exports=function(e,t,n,i){try{return i?t(r(n)[0],n[1]):t(n)}catch(s){throw o(e),s}}},"9bf2":function(e,t,n){var r=n("83ab"),o=n("0cfb"),i=n("825a"),s=n("c04e"),a=Object.defineProperty;t.f=r?a:function(e,t,n){if(i(e),t=s(t,!0),i(n),o)try{return a(e,t,n)}catch(r){}if("get"in n||"set"in n)throw TypeError("Accessors not supported");return"value"in n&&(e[t]=n.value),e}},"9ed3":function(e,t,n){"use strict";var r=n("ae93").IteratorPrototype,o=n("7c73"),i=n("5c6c"),s=n("d44e"),a=n("3f8c"),c=function(){return this};e.exports=function(e,t,n){var u=t+" Iterator";return e.prototype=o(r,{next:i(1,n)}),s(e,u,!1,!0),a[u]=c,e}},"9f7f":function(e,t,n){"use strict";var r=n("d039");function o(e,t){return RegExp(e,t)}t.UNSUPPORTED_Y=r((function(){var e=o("a","y");return e.lastIndex=2,null!=e.exec("abcd")})),t.BROKEN_CARET=r((function(){var e=o("^r","gy");return e.lastIndex=2,null!=e.exec("str")}))},a15b:function(e,t,n){"use strict";var r=n("23e7"),o=n("44ad"),i=n("fc6a"),s=n("a640"),a=[].join,c=o!=Object,u=s("join",",");r({target:"Array",proto:!0,forced:c||!u},{join:function(e){return a.call(i(this),void 0===e?",":e)}})},a4d3:function(e,t,n){"use strict";var r=n("23e7"),o=n("da84"),i=n("d066"),s=n("c430"),a=n("83ab"),c=n("4930"),u=n("fdbf"),p=n("d039"),f=n("5135"),l=n("e8b5"),h=n("861d"),d=n("825a"),y=n("7b0b"),x=n("fc6a"),m=n("c04e"),g=n("5c6c"),w=n("7c73"),_=n("df75"),v=n("241c"),b=n("057f"),E=n("7418"),j=n("06cf"),k=n("9bf2"),S=n("d1e7"),O=n("9112"),P=n("6eeb"),T=n("5692"),D=n("f772"),q=n("d012"),A=n("90e3"),R=n("b622"),C=n("e538"),L=n("746f"),I=n("d44e"),M=n("69f3"),N=n("b727").forEach,F=D("hidden"),B="Symbol",$="prototype",H=R("toPrimitive"),G=M.set,W=M.getterFor(B),U=Object[$],K=o.Symbol,Y=i("JSON","stringify"),V=j.f,J=k.f,X=b.f,z=S.f,Q=T("symbols"),Z=T("op-symbols"),ee=T("string-to-symbol-registry"),te=T("symbol-to-string-registry"),ne=T("wks"),re=o.QObject,oe=!re||!re[$]||!re[$].findChild,ie=a&&p((function(){return 7!=w(J({},"a",{get:function(){return J(this,"a",{value:7}).a}})).a}))?function(e,t,n){var r=V(U,t);r&&delete U[t],J(e,t,n),r&&e!==U&&J(U,t,r)}:J,se=function(e,t){var n=Q[e]=w(K[$]);return G(n,{type:B,tag:e,description:t}),a||(n.description=t),n},ae=u?function(e){return"symbol"==typeof e}:function(e){return Object(e)instanceof K},ce=function(e,t,n){e===U&&ce(Z,t,n),d(e);var r=m(t,!0);return d(n),f(Q,r)?(n.enumerable?(f(e,F)&&e[F][r]&&(e[F][r]=!1),n=w(n,{enumerable:g(0,!1)})):(f(e,F)||J(e,F,g(1,{})),e[F][r]=!0),ie(e,r,n)):J(e,r,n)},ue=function(e,t){d(e);var n=x(t),r=_(n).concat(de(n));return N(r,(function(t){a&&!fe.call(n,t)||ce(e,t,n[t])})),e},pe=function(e,t){return void 0===t?w(e):ue(w(e),t)},fe=function(e){var t=m(e,!0),n=z.call(this,t);return!(this===U&&f(Q,t)&&!f(Z,t))&&(!(n||!f(this,t)||!f(Q,t)||f(this,F)&&this[F][t])||n)},le=function(e,t){var n=x(e),r=m(t,!0);if(n!==U||!f(Q,r)||f(Z,r)){var o=V(n,r);return!o||!f(Q,r)||f(n,F)&&n[F][r]||(o.enumerable=!0),o}},he=function(e){var t=X(x(e)),n=[];return N(t,(function(e){f(Q,e)||f(q,e)||n.push(e)})),n},de=function(e){var t=e===U,n=X(t?Z:x(e)),r=[];return N(n,(function(e){!f(Q,e)||t&&!f(U,e)||r.push(Q[e])})),r};if(c||(K=function(){if(this instanceof K)throw TypeError("Symbol is not a constructor");var e=arguments.length&&void 0!==arguments[0]?String(arguments[0]):void 0,t=A(e),n=function(e){this===U&&n.call(Z,e),f(this,F)&&f(this[F],t)&&(this[F][t]=!1),ie(this,t,g(1,e))};return a&&oe&&ie(U,t,{configurable:!0,set:n}),se(t,e)},P(K[$],"toString",(function(){return W(this).tag})),P(K,"withoutSetter",(function(e){return se(A(e),e)})),S.f=fe,k.f=ce,j.f=le,v.f=b.f=he,E.f=de,C.f=function(e){return se(R(e),e)},a&&(J(K[$],"description",{configurable:!0,get:function(){return W(this).description}}),s||P(U,"propertyIsEnumerable",fe,{unsafe:!0}))),r({global:!0,wrap:!0,forced:!c,sham:!c},{Symbol:K}),N(_(ne),(function(e){L(e)})),r({target:B,stat:!0,forced:!c},{for:function(e){var t=String(e);if(f(ee,t))return ee[t];var n=K(t);return ee[t]=n,te[n]=t,n},keyFor:function(e){if(!ae(e))throw TypeError(e+" is not a symbol");if(f(te,e))return te[e]},useSetter:function(){oe=!0},useSimple:function(){oe=!1}}),r({target:"Object",stat:!0,forced:!c,sham:!a},{create:pe,defineProperty:ce,defineProperties:ue,getOwnPropertyDescriptor:le}),r({target:"Object",stat:!0,forced:!c},{getOwnPropertyNames:he,getOwnPropertySymbols:de}),r({target:"Object",stat:!0,forced:p((function(){E.f(1)}))},{getOwnPropertySymbols:function(e){return E.f(y(e))}}),Y){var ye=!c||p((function(){var e=K();return"[null]"!=Y([e])||"{}"!=Y({a:e})||"{}"!=Y(Object(e))}));r({target:"JSON",stat:!0,forced:ye},{stringify:function(e,t,n){var r,o=[e],i=1;while(arguments.length>i)o.push(arguments[i++]);if(r=t,(h(t)||void 0!==e)&&!ae(e))return l(t)||(t=function(e,t){if("function"==typeof r&&(t=r.call(this,e,t)),!ae(t))return t}),o[1]=t,Y.apply(null,o)}})}K[$][H]||O(K[$],H,K[$].valueOf),I(K,B),q[F]=!0},a630:function(e,t,n){var r=n("23e7"),o=n("4df4"),i=n("1c7e"),s=!i((function(e){Array.from(e)}));r({target:"Array",stat:!0,forced:s},{from:o})},a640:function(e,t,n){"use strict";var r=n("d039");e.exports=function(e,t){var n=[][e];return!!n&&r((function(){n.call(null,t||function(){throw 1},1)}))}},a691:function(e,t){var n=Math.ceil,r=Math.floor;e.exports=function(e){return isNaN(e=+e)?0:(e>0?r:n)(e)}},a9e3:function(e,t,n){"use strict";var r=n("83ab"),o=n("da84"),i=n("94ca"),s=n("6eeb"),a=n("5135"),c=n("c6b6"),u=n("7156"),p=n("c04e"),f=n("d039"),l=n("7c73"),h=n("241c").f,d=n("06cf").f,y=n("9bf2").f,x=n("58a8").trim,m="Number",g=o[m],w=g.prototype,_=c(l(w))==m,v=function(e){var t,n,r,o,i,s,a,c,u=p(e,!1);if("string"==typeof u&&u.length>2)if(u=x(u),t=u.charCodeAt(0),43===t||45===t){if(n=u.charCodeAt(2),88===n||120===n)return NaN}else if(48===t){switch(u.charCodeAt(1)){case 66:case 98:r=2,o=49;break;case 79:case 111:r=8,o=55;break;default:return+u}for(i=u.slice(2),s=i.length,a=0;a<s;a++)if(c=i.charCodeAt(a),c<48||c>o)return NaN;return parseInt(i,r)}return+u};if(i(m,!g(" 0o1")||!g("0b1")||g("+0x1"))){for(var b,E=function(e){var t=arguments.length<1?0:e,n=this;return n instanceof E&&(_?f((function(){w.valueOf.call(n)})):c(n)!=m)?u(new g(v(t)),n,E):v(t)},j=r?h(g):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger,fromString,range".split(","),k=0;j.length>k;k++)a(g,b=j[k])&&!a(E,b)&&y(E,b,d(g,b));E.prototype=w,w.constructor=E,s(o,m,E)}},ac1f:function(e,t,n){"use strict";var r=n("23e7"),o=n("9263");r({target:"RegExp",proto:!0,forced:/./.exec!==o},{exec:o})},ad6d:function(e,t,n){"use strict";var r=n("825a");e.exports=function(){var e=r(this),t="";return e.global&&(t+="g"),e.ignoreCase&&(t+="i"),e.multiline&&(t+="m"),e.dotAll&&(t+="s"),e.unicode&&(t+="u"),e.sticky&&(t+="y"),t}},ae93:function(e,t,n){"use strict";var r,o,i,s=n("d039"),a=n("e163"),c=n("9112"),u=n("5135"),p=n("b622"),f=n("c430"),l=p("iterator"),h=!1,d=function(){return this};[].keys&&(i=[].keys(),"next"in i?(o=a(a(i)),o!==Object.prototype&&(r=o)):h=!0);var y=void 0==r||s((function(){var e={};return r[l].call(e)!==e}));y&&(r={}),f&&!y||u(r,l)||c(r,l,d),e.exports={IteratorPrototype:r,BUGGY_SAFARI_ITERATORS:h}},b041:function(e,t,n){"use strict";var r=n("00ee"),o=n("f5df");e.exports=r?{}.toString:function(){return"[object "+o(this)+"]"}},b0c0:function(e,t,n){var r=n("83ab"),o=n("9bf2").f,i=Function.prototype,s=i.toString,a=/^\s*function ([^ (]*)/,c="name";r&&!(c in i)&&o(i,c,{configurable:!0,get:function(){try{return s.call(this).match(a)[1]}catch(e){return""}}})},b622:function(e,t,n){var r=n("da84"),o=n("5692"),i=n("5135"),s=n("90e3"),a=n("4930"),c=n("fdbf"),u=o("wks"),p=r.Symbol,f=c?p:p&&p.withoutSetter||s;e.exports=function(e){return i(u,e)&&(a||"string"==typeof u[e])||(a&&i(p,e)?u[e]=p[e]:u[e]=f("Symbol."+e)),u[e]}},b64b:function(e,t,n){var r=n("23e7"),o=n("7b0b"),i=n("df75"),s=n("d039"),a=s((function(){i(1)}));r({target:"Object",stat:!0,forced:a},{keys:function(e){return i(o(e))}})},b727:function(e,t,n){var r=n("0366"),o=n("44ad"),i=n("7b0b"),s=n("50c4"),a=n("65f0"),c=[].push,u=function(e){var t=1==e,n=2==e,u=3==e,p=4==e,f=6==e,l=7==e,h=5==e||f;return function(d,y,x,m){for(var g,w,_=i(d),v=o(_),b=r(y,x,3),E=s(v.length),j=0,k=m||a,S=t?k(d,E):n||l?k(d,0):void 0;E>j;j++)if((h||j in v)&&(g=v[j],w=b(g,j,_),e))if(t)S[j]=w;else if(w)switch(e){case 3:return!0;case 5:return g;case 6:return j;case 2:c.call(S,g)}else switch(e){case 4:return!1;case 7:c.call(S,g)}return f?-1:u||p?p:S}};e.exports={forEach:u(0),map:u(1),filter:u(2),some:u(3),every:u(4),find:u(5),findIndex:u(6),filterOut:u(7)}},c04e:function(e,t,n){var r=n("861d");e.exports=function(e,t){if(!r(e))return e;var n,o;if(t&&"function"==typeof(n=e.toString)&&!r(o=n.call(e)))return o;if("function"==typeof(n=e.valueOf)&&!r(o=n.call(e)))return o;if(!t&&"function"==typeof(n=e.toString)&&!r(o=n.call(e)))return o;throw TypeError("Can't convert object to primitive value")}},c1fd:function(e){e.exports=JSON.parse('["/::)","/::~","/::B","/::|","/:8-)","/::<","/::$","/::X","/::Z","/::\'(","/::-|","/::@","/::P","/::D","/::O","/::(","[Blush]","/::Q","/::T","/:,@P","/:,@-D","/::d","/:,@o","/:|-)","/::!","/::>","/::,@","/::-S","/:?","/:,@x","/:,@@","/:,@!","/:!!!","/:xx","[Bye]","/:wipe","/:dig","/:handclap","/:B-)","/:@>","/:>-|","/:P-(","/::\'|","/:X-)","/::*","/:8*","[Happy]","[Sick]","[Flushed]","[Lol]","[Terror]","[LetDown]","[Duh]","[Hey]","[Facepalm]","[Smirk]","[Smart]","[Concerned]","[Yeah!]","[Onlooker]","[GoForIt]","[Sweats]","[OMG]","[Emm]","[Respect]","[Doge]","[NoProb]","[MyBad]","[Wow]","[Boring]","[666]","[LetMeSee]","[Sigh]","[Hurt]","[Broken]","/:showlove","/:heart","/:break","/:hug","/:strong","/:weak","/:share","/:v","[Salute]","/:jj","/:@@","/:ok","[Worship]","/:beer","/:coffee","/:cake","/:rose","/:fade","/:pd","/:bome","/:shit","/:moon","/:sun","[Party]","[Gift]","[Packet]","[Rich]","[Blessing]","[Fireworks]","[Firecracker]","/:pig","/:jump","/:shake","/:circle"]')},c430:function(e,t){e.exports=!1},c6b6:function(e,t){var n={}.toString;e.exports=function(e){return n.call(e).slice(8,-1)}},c6cd:function(e,t,n){var r=n("da84"),o=n("ce4e"),i="__core-js_shared__",s=r[i]||o(i,{});e.exports=s},c8ba:function(e,t){var n;n=function(){return this}();try{n=n||new Function("return this")()}catch(r){"object"===typeof window&&(n=window)}e.exports=n},c8d2:function(e,t,n){var r=n("d039"),o=n("5899"),i="​᠎";e.exports=function(e){return r((function(){return!!o[e]()||i[e]()!=i||o[e].name!==e}))}},ca84:function(e,t,n){var r=n("5135"),o=n("fc6a"),i=n("4d64").indexOf,s=n("d012");e.exports=function(e,t){var n,a=o(e),c=0,u=[];for(n in a)!r(s,n)&&r(a,n)&&u.push(n);while(t.length>c)r(a,n=t[c++])&&(~i(u,n)||u.push(n));return u}},cc12:function(e,t,n){var r=n("da84"),o=n("861d"),i=r.document,s=o(i)&&o(i.createElement);e.exports=function(e){return s?i.createElement(e):{}}},ce4e:function(e,t,n){var r=n("da84"),o=n("9112");e.exports=function(e,t){try{o(r,e,t)}catch(n){r[e]=t}return t}},d012:function(e,t){e.exports={}},d039:function(e,t){e.exports=function(e){try{return!!e()}catch(t){return!0}}},d066:function(e,t,n){var r=n("428f"),o=n("da84"),i=function(e){return"function"==typeof e?e:void 0};e.exports=function(e,t){return arguments.length<2?i(r[e])||i(o[e]):r[e]&&r[e][t]||o[e]&&o[e][t]}},d1e7:function(e,t,n){"use strict";var r={}.propertyIsEnumerable,o=Object.getOwnPropertyDescriptor,i=o&&!r.call({1:2},1);t.f=i?function(e){var t=o(this,e);return!!t&&t.enumerable}:r},d28b:function(e,t,n){var r=n("746f");r("iterator")},d2bb:function(e,t,n){var r=n("825a"),o=n("3bbe");e.exports=Object.setPrototypeOf||("__proto__"in{}?function(){var e,t=!1,n={};try{e=Object.getOwnPropertyDescriptor(Object.prototype,"__proto__").set,e.call(n,[]),t=n instanceof Array}catch(i){}return function(n,i){return r(n),o(i),t?e.call(n,i):n.__proto__=i,n}}():void 0)},d3b7:function(e,t,n){var r=n("00ee"),o=n("6eeb"),i=n("b041");r||o(Object.prototype,"toString",i,{unsafe:!0})},d44e:function(e,t,n){var r=n("9bf2").f,o=n("5135"),i=n("b622"),s=i("toStringTag");e.exports=function(e,t,n){e&&!o(e=n?e:e.prototype,s)&&r(e,s,{configurable:!0,value:t})}},d58f:function(e,t,n){var r=n("1c0b"),o=n("7b0b"),i=n("44ad"),s=n("50c4"),a=function(e){return function(t,n,a,c){r(n);var u=o(t),p=i(u),f=s(u.length),l=e?f-1:0,h=e?-1:1;if(a<2)while(1){if(l in p){c=p[l],l+=h;break}if(l+=h,e?l<0:f<=l)throw TypeError("Reduce of empty array with no initial value")}for(;e?l>=0:f>l;l+=h)l in p&&(c=n(c,p[l],l,u));return c}};e.exports={left:a(!1),right:a(!0)}},d784:function(e,t,n){"use strict";n("ac1f");var r=n("6eeb"),o=n("d039"),i=n("b622"),s=n("9263"),a=n("9112"),c=i("species"),u=!o((function(){var e=/./;return e.exec=function(){var e=[];return e.groups={a:"7"},e},"7"!=="".replace(e,"$<a>")})),p=function(){return"$0"==="a".replace(/./,"$0")}(),f=i("replace"),l=function(){return!!/./[f]&&""===/./[f]("a","$0")}(),h=!o((function(){var e=/(?:)/,t=e.exec;e.exec=function(){return t.apply(this,arguments)};var n="ab".split(e);return 2!==n.length||"a"!==n[0]||"b"!==n[1]}));e.exports=function(e,t,n,f){var d=i(e),y=!o((function(){var t={};return t[d]=function(){return 7},7!=""[e](t)})),x=y&&!o((function(){var t=!1,n=/a/;return"split"===e&&(n={},n.constructor={},n.constructor[c]=function(){return n},n.flags="",n[d]=/./[d]),n.exec=function(){return t=!0,null},n[d](""),!t}));if(!y||!x||"replace"===e&&(!u||!p||l)||"split"===e&&!h){var m=/./[d],g=n(d,""[e],(function(e,t,n,r,o){return t.exec===s?y&&!o?{done:!0,value:m.call(t,n,r)}:{done:!0,value:e.call(n,t,r)}:{done:!1}}),{REPLACE_KEEPS_$0:p,REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE:l}),w=g[0],_=g[1];r(String.prototype,e,w),r(RegExp.prototype,d,2==t?function(e,t){return _.call(e,this,t)}:function(e){return _.call(e,this)})}f&&a(RegExp.prototype[d],"sham",!0)}},d81d:function(e,t,n){"use strict";var r=n("23e7"),o=n("b727").map,i=n("1dde"),s=i("map");r({target:"Array",proto:!0,forced:!s},{map:function(e){return o(this,e,arguments.length>1?arguments[1]:void 0)}})},da84:function(e,t,n){(function(t){var n=function(e){return e&&e.Math==Math&&e};e.exports=n("object"==typeof globalThis&&globalThis)||n("object"==typeof window&&window)||n("object"==typeof self&&self)||n("object"==typeof t&&t)||function(){return this}()||Function("return this")()}).call(this,n("c8ba"))},dbb4:function(e,t,n){var r=n("23e7"),o=n("83ab"),i=n("56ef"),s=n("fc6a"),a=n("06cf"),c=n("8418");r({target:"Object",stat:!0,sham:!o},{getOwnPropertyDescriptors:function(e){var t,n,r=s(e),o=a.f,u=i(r),p={},f=0;while(u.length>f)n=o(r,t=u[f++]),void 0!==n&&c(p,t,n);return p}})},ddb0:function(e,t,n){var r=n("da84"),o=n("fdbc"),i=n("e260"),s=n("9112"),a=n("b622"),c=a("iterator"),u=a("toStringTag"),p=i.values;for(var f in o){var l=r[f],h=l&&l.prototype;if(h){if(h[c]!==p)try{s(h,c,p)}catch(y){h[c]=p}if(h[u]||s(h,u,f),o[f])for(var d in i)if(h[d]!==i[d])try{s(h,d,i[d])}catch(y){h[d]=i[d]}}}},ded3:function(e,t,n){n("b64b"),n("a4d3"),n("4de4"),n("e439"),n("159b"),n("dbb4");var r=n("9523");function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}e.exports=i,e.exports["default"]=e.exports,e.exports.__esModule=!0},df75:function(e,t,n){var r=n("ca84"),o=n("7839");e.exports=Object.keys||function(e){return r(e,o)}},e01a:function(e,t,n){"use strict";var r=n("23e7"),o=n("83ab"),i=n("da84"),s=n("5135"),a=n("861d"),c=n("9bf2").f,u=n("e893"),p=i.Symbol;if(o&&"function"==typeof p&&(!("description"in p.prototype)||void 0!==p().description)){var f={},l=function(){var e=arguments.length<1||void 0===arguments[0]?void 0:String(arguments[0]),t=this instanceof l?new p(e):void 0===e?p():p(e);return""===e&&(f[t]=!0),t};u(l,p);var h=l.prototype=p.prototype;h.constructor=l;var d=h.toString,y="Symbol(test)"==String(p("test")),x=/^Symbol\((.*)\)[^)]+$/;c(h,"description",{configurable:!0,get:function(){var e=a(this)?this.valueOf():this,t=d.call(e);if(s(f,e))return"";var n=y?t.slice(7,-1):t.replace(x,"$1");return""===n?void 0:n}}),r({global:!0,forced:!0},{Symbol:l})}},e163:function(e,t,n){var r=n("5135"),o=n("7b0b"),i=n("f772"),s=n("e177"),a=i("IE_PROTO"),c=Object.prototype;e.exports=s?Object.getPrototypeOf:function(e){return e=o(e),r(e,a)?e[a]:"function"==typeof e.constructor&&e instanceof e.constructor?e.constructor.prototype:e instanceof Object?c:null}},e177:function(e,t,n){var r=n("d039");e.exports=!r((function(){function e(){}return e.prototype.constructor=null,Object.getPrototypeOf(new e)!==e.prototype}))},e260:function(e,t,n){"use strict";var r=n("fc6a"),o=n("44d2"),i=n("3f8c"),s=n("69f3"),a=n("7dd0"),c="Array Iterator",u=s.set,p=s.getterFor(c);e.exports=a(Array,"Array",(function(e,t){u(this,{type:c,target:r(e),index:0,kind:t})}),(function(){var e=p(this),t=e.target,n=e.kind,r=e.index++;return!t||r>=t.length?(e.target=void 0,{value:void 0,done:!0}):"keys"==n?{value:r,done:!1}:"values"==n?{value:t[r],done:!1}:{value:[r,t[r]],done:!1}}),"values"),i.Arguments=i.Array,o("keys"),o("values"),o("entries")},e439:function(e,t,n){var r=n("23e7"),o=n("d039"),i=n("fc6a"),s=n("06cf").f,a=n("83ab"),c=o((function(){s(1)})),u=!a||c;r({target:"Object",stat:!0,forced:u,sham:!a},{getOwnPropertyDescriptor:function(e,t){return s(i(e),t)}})},e538:function(e,t,n){var r=n("b622");t.f=r},e893:function(e,t,n){var r=n("5135"),o=n("56ef"),i=n("06cf"),s=n("9bf2");e.exports=function(e,t){for(var n=o(t),a=s.f,c=i.f,u=0;u<n.length;u++){var p=n[u];r(e,p)||a(e,p,c(t,p))}}},e8b5:function(e,t,n){var r=n("c6b6");e.exports=Array.isArray||function(e){return"Array"==r(e)}},e95a:function(e,t,n){var r=n("b622"),o=n("3f8c"),i=r("iterator"),s=Array.prototype;e.exports=function(e){return void 0!==e&&(o.Array===e||s[i]===e)}},f5df:function(e,t,n){var r=n("00ee"),o=n("c6b6"),i=n("b622"),s=i("toStringTag"),a="Arguments"==o(function(){return arguments}()),c=function(e,t){try{return e[t]}catch(n){}};e.exports=r?o:function(e){var t,n,r;return void 0===e?"Undefined":null===e?"Null":"string"==typeof(n=c(t=Object(e),s))?n:a?o(t):"Object"==(r=o(t))&&"function"==typeof t.callee?"Arguments":r}},f601:function(e,t,n){var r=n("ded3").default;n("d81d"),n("13d5");var o=n("8c94"),i=n("c1fd"),s=["key","old","cn","qq","en","tw","th","emoji"],a=o.map((function(e){return r({},e)})),c=a.reduce((function(e,t,n){var o=r({},e);return s.forEach((function(e){t[e]&&!o[t[e]]&&(o[t[e]]={index:n})})),o}),{}),u=i.map((function(e){return a[c[e].index]}));t.EmojiData=a,t.EmojiPanelData=u,t.EmojiDataMap=c,e.exports={EmojiData:a,EmojiPanelData:u,EmojiDataMap:c}},f772:function(e,t,n){var r=n("5692"),o=n("90e3"),i=r("keys");e.exports=function(e){return i[e]||(i[e]=o(e))}},f84d:function(e,t,n){},fb15:function(e,t,n){"use strict";if(n.r(t),n.d(t,"Icon",(function(){return g})),n.d(t,"Parser",(function(){return L})),n.d(t,"install",(function(){return W})),n.d(t,"decode",(function(){return R})),n.d(t,"split",(function(){return A})),n.d(t,"EmojiData",(function(){return f["EmojiData"]})),n.d(t,"EmojiDataMap",(function(){return f["EmojiDataMap"]})),n.d(t,"EmojiPanelData",(function(){return f["EmojiPanelData"]})),n.d(t,"Panel",(function(){return H})),"undefined"!==typeof window){var r=window.document.currentScript,o=n("8875");r=o(),"currentScript"in document||Object.defineProperty(document,"currentScript",{get:o});var i=r&&r.src.match(/(.+\/)[^/]+\.js(\?.*)?$/);i&&(n.p=i[1])}n("b64b"),n("a4d3"),n("4de4"),n("e439"),n("159b"),n("dbb4");function s(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){s(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}n("07ac"),n("b0c0");var u=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("img",{staticClass:"we-emoji",class:e.className,attrs:{src:e.picBlank,alt:e.alt}})},p=[],f=(n("5319"),n("ac1f"),n("498a"),n("7db0"),n("f601")),l=n("5e96"),h={name:"EmojiIcon",props:{name:{type:String},text:{type:String}},data:function(){return{picBlank:l["a"]}},beforeCreate:function(){var e=this.$options.propsData,t=e.name,n=e.text;t||n||console.error("emoji-icon error: Prop name or text required. Props receive:",JSON.stringify(this.$options.propsData))},computed:{emojiObj:function(){var e=this.text,t=this.name;if(e&&f["EmojiDataMap"][e]&&f["EmojiData"][f["EmojiDataMap"][e].index])return f["EmojiData"][f["EmojiDataMap"][e].index];if(t){var n=t.toLowerCase(),r=function(e){return e&&e.toLowerCase().replace(/\W+/g," ").trim().replace(/\s/g,"-")},o=f["EmojiData"].find((function(e){return r(e.en)===n}));if(o)return o}return(t||e)&&console.error("emoji-icon error: Illegal prop name or text. Props receive:",JSON.stringify(this.$options.propsData)),{}},className:function(){return this.emojiObj.style},alt:function(){return this.text}}},d=h;function y(e,t,n,r,o,i,s,a){var c,u="function"===typeof e?e.options:e;if(t&&(u.render=t,u.staticRenderFns=n,u._compiled=!0),r&&(u.functional=!0),i&&(u._scopeId="data-v-"+i),s?(c=function(e){e=e||this.$vnode&&this.$vnode.ssrContext||this.parent&&this.parent.$vnode&&this.parent.$vnode.ssrContext,e||"undefined"===typeof __VUE_SSR_CONTEXT__||(e=__VUE_SSR_CONTEXT__),o&&o.call(this,e),e&&e._registeredComponents&&e._registeredComponents.add(s)},u._ssrRegister=c):o&&(c=a?function(){o.call(this,(u.functional?this.parent:this).$root.$options.shadowRoot)}:o),c)if(u.functional){u._injectStyles=c;var p=u.render;u.render=function(e,t){return c.call(t),p(e,t)}}else{var f=u.beforeCreate;u.beforeCreate=f?[].concat(f,c):[c]}return{exports:e,options:u}}var x=y(d,u,p,!1,null,null,null),m=x.exports;m.install=function(e){e.component(m.name,m)};var g=m;function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function _(e){if(Array.isArray(e))return w(e)}n("e01a"),n("d3b7"),n("d28b"),n("3ca3"),n("e260"),n("ddb0"),n("a630");function v(e){if("undefined"!==typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}n("fb6a");function b(e,t){if(e){if("string"===typeof e)return w(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?w(e,t):void 0}}function E(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function j(e){return _(e)||v(e)||b(e)||E()}n("d81d"),n("13d5"),n("99af"),n("4d63"),n("25f0"),n("a15b");var k=function(e){var t=e.className,n=e.text;return'<img src="'.concat(l["a"],'" class="we-emoji ').concat(t,'" alt="').concat(n,'">')};function S(e){return!(!f["EmojiDataMap"][e]||!f["EmojiData"][f["EmojiDataMap"][e].index])}function O(e,t,n){var r,o=new RegExp(t,"g");while(r=o.exec(e))for(var i=r,s=i[0],a=i.index,c=n.length;c<=s.length;++c){var u=s.slice(0,c);if(S(u))return{0:u,index:a}}return null}function P(e){var t,n=new RegExp(/\[[^[\]]+\]/,"g");while(t=n.exec(e))if(S(t[0]))return t;return null}function T(e){var t=/(\ud83c[\udf00-\udfff])|(\ud83d[\udc00-\ude4f\ude80-\udeff])|[\u2600-\u2B55]/;return P(e)||O(e,/\/([\u4e00-\u9fa5\w]{1,4})/,"/")||O(e,/\/(:[^/]{1,8})/,"/:")||O(e,t,"")}function D(e){return e}function q(e){if(!e)return[];var t=T(e);if(t){var n=t[0],r=t.index,o=e.slice(0,r),i=e.slice(r+n.length),s=S(n)?{text:n,data:f["EmojiData"][f["EmojiDataMap"][n].index]}:n,a=[].concat(j(q(o)),[s],j(q(i)));return a.some((function(e){return e.text}))?a:[a.join("")]}return[e]}var A=function(e,t){var n=D(e,t);return q(n)},R=function(e,t){return e?A(e,t).map((function(e){return e.text?k({text:e.text,className:e.data.style}):e})).join(""):e},C={name:"EmojiParser",props:{tag:{type:String,default:"span"}},methods:{replace:function(e){var t=this,n=this.$createElement;return e&&e.length?e.map((function(e){var r=e.text;if(!r){var o=function(e){return e&&e.reduce((function(e,t){return Array.isArray(t)?[].concat(j(e),j(t)):[].concat(j(e),[t])}),[])};return c(c({},e),{},{children:o(t.replace(e.children))})}return A(r).map((function(e){return e.text?n(g,{attrs:{text:e.text}}):t._v(e)}))})):e}},render:function(e){return e(this.tag,this.replace(this.$slots.default))},install:function(e){e.component(C.name,C)}},L=C,I=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"emotion_panel"},[n("ul",{staticClass:"emotions",attrs:{slot:"content"},slot:"content"},e._l(e.edata,(function(t,r){return n("li",{key:t.key,staticClass:"emotions_item",on:{click:function(t){return e.select(r)}}},[n("emoji-icon",{attrs:{text:t.cn}})],1)})),0)])},M=[],N=(n("a9e3"),{name:"EmojiPanel",props:{emojiPanelWidth:{type:Number,default:300},emojiPanelHeight:{type:Number,default:300}},data:function(){return{edata:f["EmojiPanelData"]}},methods:{select:function(e){this.$emit("select",this.edata[e])}}}),F=N,B=y(F,I,M,!1,null,null,null),$=B.exports;$.install=function(e){e.component($.name,$)};var H=$,G=(n("f84d"),{Icon:g,Parser:L,Panel:H}),W=function e(t){e.installed||(e.installed=!0,Object.values(G).forEach((function(e){t.component(e.name,e)})))},U=c(c({},G),{},{install:W,decode:R,split:A,EmojiData:f["EmojiData"],EmojiDataMap:f["EmojiDataMap"],EmojiPanelData:f["EmojiPanelData"]});"undefined"!==typeof window&&window.Vue&&W(window.Vue);var K=U;t["default"]=K},fb6a:function(e,t,n){"use strict";var r=n("23e7"),o=n("861d"),i=n("e8b5"),s=n("23cb"),a=n("50c4"),c=n("fc6a"),u=n("8418"),p=n("b622"),f=n("1dde"),l=f("slice"),h=p("species"),d=[].slice,y=Math.max;r({target:"Array",proto:!0,forced:!l},{slice:function(e,t){var n,r,p,f=c(this),l=a(f.length),x=s(e,l),m=s(void 0===t?l:t,l);if(i(f)&&(n=f.constructor,"function"!=typeof n||n!==Array&&!i(n.prototype)?o(n)&&(n=n[h],null===n&&(n=void 0)):n=void 0,n===Array||void 0===n))return d.call(f,x,m);for(r=new(void 0===n?Array:n)(y(m-x,0)),p=0;x<m;x++,p++)x in f&&u(r,p,f[x]);return r.length=p,r}})},fc6a:function(e,t,n){var r=n("44ad"),o=n("1d80");e.exports=function(e){return r(o(e))}},fdbc:function(e,t){e.exports={CSSRuleList:0,CSSStyleDeclaration:0,CSSValueList:0,ClientRectList:0,DOMRectList:0,DOMStringList:0,DOMTokenList:1,DataTransferItemList:0,FileList:0,HTMLAllCollection:0,HTMLCollection:0,HTMLFormElement:0,HTMLSelectElement:0,MediaList:0,MimeTypeArray:0,NamedNodeMap:0,NodeList:1,PaintRequestList:0,Plugin:0,PluginArray:0,SVGLengthList:0,SVGNumberList:0,SVGPathSegList:0,SVGPointList:0,SVGStringList:0,SVGTransformList:0,SourceBufferList:0,StyleSheetList:0,TextTrackCueList:0,TextTrackList:0,TouchList:0}},fdbf:function(e,t,n){var r=n("4930");e.exports=r&&!Symbol.sham&&"symbol"==typeof Symbol.iterator}})["default"]}));</script><script h5only type="text/javascript" nonce="1682091926" reportloaderror>!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define("Darkmode",[],t):"object"==typeof exports?exports.Darkmode=t():e.Darkmode=t()}(window,(function(){return function(e){var t={};function r(n){if(t[n])return t[n].exports;var a=t[n]={i:n,l:!1,exports:{}};return e[n].call(a.exports,a,a.exports,r),a.l=!0,a.exports}return r.m=e,r.c=t,r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},r.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)r.d(n,a,function(t){return e[t]}.bind(null,a));return n},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=9)}([function(e,t,r){"use strict";var n=r(3),a=r(6),o=[].slice,i=["keyword","gray","hex"],l={};Object.keys(a).forEach((function(e){l[o.call(a[e].labels).sort().join("")]=e}));var s={};function u(e,t){if(!(this instanceof u))return new u(e,t);if(t&&t in i&&(t=null),t&&!(t in a))throw new Error("Unknown model: "+t);var r,c;if(null==e)this.model="rgb",this.color=[0,0,0],this.valpha=1;else if(e instanceof u)this.model=e.model,this.color=e.color.slice(),this.valpha=e.valpha;else if("string"==typeof e){var h=n.get(e);if(null===h)throw new Error("Unable to parse color from string: "+e);this.model=h.model,c=a[this.model].channels,this.color=h.value.slice(0,c),this.valpha="number"==typeof h.value[c]?h.value[c]:1}else if(e.length){this.model=t||"rgb",c=a[this.model].channels;var f=o.call(e,0,c);this.color=d(f,c),this.valpha="number"==typeof e[c]?e[c]:1}else if("number"==typeof e)e&=16777215,this.model="rgb",this.color=[e>>16&255,e>>8&255,255&e],this.valpha=1;else{this.valpha=1;var g=Object.keys(e);"alpha"in e&&(g.splice(g.indexOf("alpha"),1),this.valpha="number"==typeof e.alpha?e.alpha:0);var b=g.sort().join("");if(!(b in l))throw new Error("Unable to parse color from object: "+JSON.stringify(e));this.model=l[b];var p=a[this.model].labels,y=[];for(r=0;r<p.length;r++)y.push(e[p[r]]);this.color=d(y)}if(s[this.model])for(c=a[this.model].channels,r=0;r<c;r++){var m=s[this.model][r];m&&(this.color[r]=m(this.color[r]))}this.valpha=Math.max(0,Math.min(1,this.valpha)),Object.freeze&&Object.freeze(this)}function c(e,t,r){return(e=Array.isArray(e)?e:[e]).forEach((function(e){(s[e]||(s[e]=[]))[t]=r})),e=e[0],function(n){var a;return arguments.length?(r&&(n=r(n)),(a=this[e]()).color[t]=n,a):(a=this[e]().color[t],r&&(a=r(a)),a)}}function h(e){return function(t){return Math.max(0,Math.min(e,t))}}function f(e){return Array.isArray(e)?e:[e]}function d(e,t){for(var r=0;r<t;r++)"number"!=typeof e[r]&&(e[r]=0);return e}u.prototype={toString:function(){return this.string()},toJSON:function(){return this[this.model]()},string:function(e){var t=this.model in n.to?this:this.rgb(),r=1===(t=t.round("number"==typeof e?e:1)).valpha?t.color:t.color.concat(this.valpha);return n.to[t.model](r)},percentString:function(e){var t=this.rgb().round("number"==typeof e?e:1),r=1===t.valpha?t.color:t.color.concat(this.valpha);return n.to.rgb.percent(r)},array:function(){return 1===this.valpha?this.color.slice():this.color.concat(this.valpha)},object:function(){for(var e={},t=a[this.model].channels,r=a[this.model].labels,n=0;n<t;n++)e[r[n]]=this.color[n];return 1!==this.valpha&&(e.alpha=this.valpha),e},unitArray:function(){var e=this.rgb().color;return e[0]/=255,e[1]/=255,e[2]/=255,1!==this.valpha&&e.push(this.valpha),e},unitObject:function(){var e=this.rgb().object();return e.r/=255,e.g/=255,e.b/=255,1!==this.valpha&&(e.alpha=this.valpha),e},round:function(e){return e=Math.max(e||0,0),new u(this.color.map(function(e){return function(t){return function(e,t){return Number(e.toFixed(t))}(t,e)}}(e)).concat(this.valpha),this.model)},alpha:function(e){return arguments.length?new u(this.color.concat(Math.max(0,Math.min(1,e))),this.model):this.valpha},red:c("rgb",0,h(255)),green:c("rgb",1,h(255)),blue:c("rgb",2,h(255)),hue:c(["hsl","hsv","hsl","hwb","hcg"],0,(function(e){return(e%360+360)%360})),saturationl:c("hsl",1,h(100)),lightness:c("hsl",2,h(100)),saturationv:c("hsv",1,h(100)),value:c("hsv",2,h(100)),chroma:c("hcg",1,h(100)),gray:c("hcg",2,h(100)),white:c("hwb",1,h(100)),wblack:c("hwb",2,h(100)),cyan:c("cmyk",0,h(100)),magenta:c("cmyk",1,h(100)),yellow:c("cmyk",2,h(100)),black:c("cmyk",3,h(100)),x:c("xyz",0,h(100)),y:c("xyz",1,h(100)),z:c("xyz",2,h(100)),l:c("lab",0,h(100)),a:c("lab",1),b:c("lab",2),keyword:function(e){return arguments.length?new u(e):a[this.model].keyword(this.color)},hex:function(e){return arguments.length?new u(e):n.to.hex(this.rgb().round().color)},rgbNumber:function(){var e=this.rgb().color;return(255&e[0])<<16|(255&e[1])<<8|255&e[2]},luminosity:function(){for(var e=this.rgb().color,t=[],r=0;r<e.length;r++){var n=e[r]/255;t[r]=n<=.03928?n/12.92:Math.pow((n+.055)/1.055,2.4)}return.2126*t[0]+.7152*t[1]+.0722*t[2]},contrast:function(e){var t=this.luminosity(),r=e.luminosity();return t>r?(t+.05)/(r+.05):(r+.05)/(t+.05)},level:function(e){var t=this.contrast(e);return t>=7.1?"AAA":t>=4.5?"AA":""},isDark:function(){var e=this.rgb().color;return(299*e[0]+587*e[1]+114*e[2])/1e3<128},isLight:function(){return!this.isDark()},negate:function(){for(var e=this.rgb(),t=0;t<3;t++)e.color[t]=255-e.color[t];return e},lighten:function(e){var t=this.hsl();return t.color[2]+=t.color[2]*e,t},darken:function(e){var t=this.hsl();return t.color[2]-=t.color[2]*e,t},saturate:function(e){var t=this.hsl();return t.color[1]+=t.color[1]*e,t},desaturate:function(e){var t=this.hsl();return t.color[1]-=t.color[1]*e,t},whiten:function(e){var t=this.hwb();return t.color[1]+=t.color[1]*e,t},blacken:function(e){var t=this.hwb();return t.color[2]+=t.color[2]*e,t},grayscale:function(){var e=this.rgb().color,t=.3*e[0]+.59*e[1]+.11*e[2];return u.rgb(t,t,t)},fade:function(e){return this.alpha(this.valpha-this.valpha*e)},opaquer:function(e){return this.alpha(this.valpha+this.valpha*e)},rotate:function(e){var t=this.hsl(),r=t.color[0];return r=(r=(r+e)%360)<0?360+r:r,t.color[0]=r,t},mix:function(e,t){if(!e||!e.rgb)throw new Error('Argument to "mix" was not a Color instance, but rather an instance of '+typeof e);var r=e.rgb(),n=this.rgb(),a=void 0===t?.5:t,o=2*a-1,i=r.alpha()-n.alpha(),l=((o*i==-1?o:(o+i)/(1+o*i))+1)/2,s=1-l;return u.rgb(l*r.red()+s*n.red(),l*r.green()+s*n.green(),l*r.blue()+s*n.blue(),r.alpha()*a+n.alpha()*(1-a))}},Object.keys(a).forEach((function(e){if(-1===i.indexOf(e)){var t=a[e].channels;u.prototype[e]=function(){if(this.model===e)return new u(this);if(arguments.length)return new u(arguments,e);var r="number"==typeof arguments[t]?t:this.valpha;return new u(f(a[this.model][e].raw(this.color)).concat(r),e)},u[e]=function(r){return"number"==typeof r&&(r=d(o.call(arguments),t)),new u(r,e)}}})),e.exports=u},function(e,t,r){"use strict";e.exports={aliceblue:[240,248,255],antiquewhite:[250,235,215],aqua:[0,255,255],aquamarine:[127,255,212],azure:[240,255,255],beige:[245,245,220],bisque:[255,228,196],black:[0,0,0],blanchedalmond:[255,235,205],blue:[0,0,255],blueviolet:[138,43,226],brown:[165,42,42],burlywood:[222,184,135],cadetblue:[95,158,160],chartreuse:[127,255,0],chocolate:[210,105,30],coral:[255,127,80],cornflowerblue:[100,149,237],cornsilk:[255,248,220],crimson:[220,20,60],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgoldenrod:[184,134,11],darkgray:[169,169,169],darkgreen:[0,100,0],darkgrey:[169,169,169],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkseagreen:[143,188,143],darkslateblue:[72,61,139],darkslategray:[47,79,79],darkslategrey:[47,79,79],darkturquoise:[0,206,209],darkviolet:[148,0,211],deeppink:[255,20,147],deepskyblue:[0,191,255],dimgray:[105,105,105],dimgrey:[105,105,105],dodgerblue:[30,144,255],firebrick:[178,34,34],floralwhite:[255,250,240],forestgreen:[34,139,34],fuchsia:[255,0,255],gainsboro:[220,220,220],ghostwhite:[248,248,255],gold:[255,215,0],goldenrod:[218,165,32],gray:[128,128,128],green:[0,128,0],greenyellow:[173,255,47],grey:[128,128,128],honeydew:[240,255,240],hotpink:[255,105,180],indianred:[205,92,92],indigo:[75,0,130],ivory:[255,255,240],khaki:[240,230,140],lavender:[230,230,250],lavenderblush:[255,240,245],lawngreen:[124,252,0],lemonchiffon:[255,250,205],lightblue:[173,216,230],lightcoral:[240,128,128],lightcyan:[224,255,255],lightgoldenrodyellow:[250,250,210],lightgray:[211,211,211],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightsalmon:[255,160,122],lightseagreen:[32,178,170],lightskyblue:[135,206,250],lightslategray:[119,136,153],lightslategrey:[119,136,153],lightsteelblue:[176,196,222],lightyellow:[255,255,224],lime:[0,255,0],limegreen:[50,205,50],linen:[250,240,230],magenta:[255,0,255],maroon:[128,0,0],mediumaquamarine:[102,205,170],mediumblue:[0,0,205],mediumorchid:[186,85,211],mediumpurple:[147,112,219],mediumseagreen:[60,179,113],mediumslateblue:[123,104,238],mediumspringgreen:[0,250,154],mediumturquoise:[72,209,204],mediumvioletred:[199,21,133],midnightblue:[25,25,112],mintcream:[245,255,250],mistyrose:[255,228,225],moccasin:[255,228,181],navajowhite:[255,222,173],navy:[0,0,128],oldlace:[253,245,230],olive:[128,128,0],olivedrab:[107,142,35],orange:[255,165,0],orangered:[255,69,0],orchid:[218,112,214],palegoldenrod:[238,232,170],palegreen:[152,251,152],paleturquoise:[175,238,238],palevioletred:[219,112,147],papayawhip:[255,239,213],peachpuff:[255,218,185],peru:[205,133,63],pink:[255,192,203],plum:[221,160,221],powderblue:[176,224,230],purple:[128,0,128],rebeccapurple:[102,51,153],red:[255,0,0],rosybrown:[188,143,143],royalblue:[65,105,225],saddlebrown:[139,69,19],salmon:[250,128,114],sandybrown:[244,164,96],seagreen:[46,139,87],seashell:[255,245,238],sienna:[160,82,45],silver:[192,192,192],skyblue:[135,206,235],slateblue:[106,90,205],slategray:[112,128,144],slategrey:[112,128,144],snow:[255,250,250],springgreen:[0,255,127],steelblue:[70,130,180],tan:[210,180,140],teal:[0,128,128],thistle:[216,191,216],tomato:[255,99,71],turquoise:[64,224,208],violet:[238,130,238],wheat:[245,222,179],white:[255,255,255],whitesmoke:[245,245,245],yellow:[255,255,0],yellowgreen:[154,205,50]}},function(e,t,r){var n=r(7),a={};for(var o in n)n.hasOwnProperty(o)&&(a[n[o]]=o);var i=e.exports={rgb:{channels:3,labels:"rgb"},hsl:{channels:3,labels:"hsl"},hsv:{channels:3,labels:"hsv"},hwb:{channels:3,labels:"hwb"},cmyk:{channels:4,labels:"cmyk"},xyz:{channels:3,labels:"xyz"},lab:{channels:3,labels:"lab"},lch:{channels:3,labels:"lch"},hex:{channels:1,labels:["hex"]},keyword:{channels:1,labels:["keyword"]},ansi16:{channels:1,labels:["ansi16"]},ansi256:{channels:1,labels:["ansi256"]},hcg:{channels:3,labels:["h","c","g"]},apple:{channels:3,labels:["r16","g16","b16"]},gray:{channels:1,labels:["gray"]}};for(var l in i)if(i.hasOwnProperty(l)){if(!("channels"in i[l]))throw new Error("missing channels property: "+l);if(!("labels"in i[l]))throw new Error("missing channel labels property: "+l);if(i[l].labels.length!==i[l].channels)throw new Error("channel and label counts mismatch: "+l);var s=i[l].channels,u=i[l].labels;delete i[l].channels,delete i[l].labels,Object.defineProperty(i[l],"channels",{value:s}),Object.defineProperty(i[l],"labels",{value:u})}i.rgb.hsl=function(e){var t,r,n=e[0]/255,a=e[1]/255,o=e[2]/255,i=Math.min(n,a,o),l=Math.max(n,a,o),s=l-i;return l===i?t=0:n===l?t=(a-o)/s:a===l?t=2+(o-n)/s:o===l&&(t=4+(n-a)/s),(t=Math.min(60*t,360))<0&&(t+=360),r=(i+l)/2,[t,100*(l===i?0:r<=.5?s/(l+i):s/(2-l-i)),100*r]},i.rgb.hsv=function(e){var t,r,n,a,o,i=e[0]/255,l=e[1]/255,s=e[2]/255,u=Math.max(i,l,s),c=u-Math.min(i,l,s),h=function(e){return(u-e)/6/c+.5};return 0===c?a=o=0:(o=c/u,t=h(i),r=h(l),n=h(s),i===u?a=n-r:l===u?a=1/3+t-n:s===u&&(a=2/3+r-t),a<0?a+=1:a>1&&(a-=1)),[360*a,100*o,100*u]},i.rgb.hwb=function(e){var t=e[0],r=e[1],n=e[2];return[i.rgb.hsl(e)[0],100*(1/255*Math.min(t,Math.min(r,n))),100*(n=1-1/255*Math.max(t,Math.max(r,n)))]},i.rgb.cmyk=function(e){var t,r=e[0]/255,n=e[1]/255,a=e[2]/255;return[100*((1-r-(t=Math.min(1-r,1-n,1-a)))/(1-t)||0),100*((1-n-t)/(1-t)||0),100*((1-a-t)/(1-t)||0),100*t]},i.rgb.keyword=function(e){var t=a[e];if(t)return t;var r,o,i,l=1/0;for(var s in n)if(n.hasOwnProperty(s)){var u=n[s],c=(o=e,i=u,Math.pow(o[0]-i[0],2)+Math.pow(o[1]-i[1],2)+Math.pow(o[2]-i[2],2));c<l&&(l=c,r=s)}return r},i.keyword.rgb=function(e){return n[e]},i.rgb.xyz=function(e){var t=e[0]/255,r=e[1]/255,n=e[2]/255;return[100*(.4124*(t=t>.04045?Math.pow((t+.055)/1.055,2.4):t/12.92)+.3576*(r=r>.04045?Math.pow((r+.055)/1.055,2.4):r/12.92)+.1805*(n=n>.04045?Math.pow((n+.055)/1.055,2.4):n/12.92)),100*(.2126*t+.7152*r+.0722*n),100*(.0193*t+.1192*r+.9505*n)]},i.rgb.lab=function(e){var t=i.rgb.xyz(e),r=t[0],n=t[1],a=t[2];return n/=100,a/=108.883,r=(r/=95.047)>.008856?Math.pow(r,1/3):7.787*r+16/116,[116*(n=n>.008856?Math.pow(n,1/3):7.787*n+16/116)-16,500*(r-n),200*(n-(a=a>.008856?Math.pow(a,1/3):7.787*a+16/116))]},i.hsl.rgb=function(e){var t,r,n,a,o,i=e[0]/360,l=e[1]/100,s=e[2]/100;if(0===l)return[o=255*s,o,o];t=2*s-(r=s<.5?s*(1+l):s+l-s*l),a=[0,0,0];for(var u=0;u<3;u++)(n=i+1/3*-(u-1))<0&&n++,n>1&&n--,o=6*n<1?t+6*(r-t)*n:2*n<1?r:3*n<2?t+(r-t)*(2/3-n)*6:t,a[u]=255*o;return a},i.hsl.hsv=function(e){var t=e[0],r=e[1]/100,n=e[2]/100,a=r,o=Math.max(n,.01);return r*=(n*=2)<=1?n:2-n,a*=o<=1?o:2-o,[t,100*(0===n?2*a/(o+a):2*r/(n+r)),100*((n+r)/2)]},i.hsv.rgb=function(e){var t=e[0]/60,r=e[1]/100,n=e[2]/100,a=Math.floor(t)%6,o=t-Math.floor(t),i=255*n*(1-r),l=255*n*(1-r*o),s=255*n*(1-r*(1-o));switch(n*=255,a){case 0:return[n,s,i];case 1:return[l,n,i];case 2:return[i,n,s];case 3:return[i,l,n];case 4:return[s,i,n];case 5:return[n,i,l]}},i.hsv.hsl=function(e){var t,r,n,a=e[0],o=e[1]/100,i=e[2]/100,l=Math.max(i,.01);return n=(2-o)*i,r=o*l,[a,100*(r=(r/=(t=(2-o)*l)<=1?t:2-t)||0),100*(n/=2)]},i.hwb.rgb=function(e){var t,r,n,a,o,i,l,s=e[0]/360,u=e[1]/100,c=e[2]/100,h=u+c;switch(h>1&&(u/=h,c/=h),n=6*s-(t=Math.floor(6*s)),0!=(1&t)&&(n=1-n),a=u+n*((r=1-c)-u),t){default:case 6:case 0:o=r,i=a,l=u;break;case 1:o=a,i=r,l=u;break;case 2:o=u,i=r,l=a;break;case 3:o=u,i=a,l=r;break;case 4:o=a,i=u,l=r;break;case 5:o=r,i=u,l=a}return[255*o,255*i,255*l]},i.cmyk.rgb=function(e){var t=e[0]/100,r=e[1]/100,n=e[2]/100,a=e[3]/100;return[255*(1-Math.min(1,t*(1-a)+a)),255*(1-Math.min(1,r*(1-a)+a)),255*(1-Math.min(1,n*(1-a)+a))]},i.xyz.rgb=function(e){var t,r,n,a=e[0]/100,o=e[1]/100,i=e[2]/100;return r=-.9689*a+1.8758*o+.0415*i,n=.0557*a+-.204*o+1.057*i,t=(t=3.2406*a+-1.5372*o+-.4986*i)>.0031308?1.055*Math.pow(t,1/2.4)-.055:12.92*t,r=r>.0031308?1.055*Math.pow(r,1/2.4)-.055:12.92*r,n=n>.0031308?1.055*Math.pow(n,1/2.4)-.055:12.92*n,[255*(t=Math.min(Math.max(0,t),1)),255*(r=Math.min(Math.max(0,r),1)),255*(n=Math.min(Math.max(0,n),1))]},i.xyz.lab=function(e){var t=e[0],r=e[1],n=e[2];return r/=100,n/=108.883,t=(t/=95.047)>.008856?Math.pow(t,1/3):7.787*t+16/116,[116*(r=r>.008856?Math.pow(r,1/3):7.787*r+16/116)-16,500*(t-r),200*(r-(n=n>.008856?Math.pow(n,1/3):7.787*n+16/116))]},i.lab.xyz=function(e){var t,r,n,a=e[0];t=e[1]/500+(r=(a+16)/116),n=r-e[2]/200;var o=Math.pow(r,3),i=Math.pow(t,3),l=Math.pow(n,3);return r=o>.008856?o:(r-16/116)/7.787,t=i>.008856?i:(t-16/116)/7.787,n=l>.008856?l:(n-16/116)/7.787,[t*=95.047,r*=100,n*=108.883]},i.lab.lch=function(e){var t,r=e[0],n=e[1],a=e[2];return(t=360*Math.atan2(a,n)/2/Math.PI)<0&&(t+=360),[r,Math.sqrt(n*n+a*a),t]},i.lch.lab=function(e){var t,r=e[0],n=e[1];return t=e[2]/360*2*Math.PI,[r,n*Math.cos(t),n*Math.sin(t)]},i.rgb.ansi16=function(e){var t=e[0],r=e[1],n=e[2],a=1 in arguments?arguments[1]:i.rgb.hsv(e)[2];if(0===(a=Math.round(a/50)))return 30;var o=30+(Math.round(n/255)<<2|Math.round(r/255)<<1|Math.round(t/255));return 2===a&&(o+=60),o},i.hsv.ansi16=function(e){return i.rgb.ansi16(i.hsv.rgb(e),e[2])},i.rgb.ansi256=function(e){var t=e[0],r=e[1],n=e[2];return t===r&&r===n?t<8?16:t>248?231:Math.round((t-8)/247*24)+232:16+36*Math.round(t/255*5)+6*Math.round(r/255*5)+Math.round(n/255*5)},i.ansi16.rgb=function(e){var t=e%10;if(0===t||7===t)return e>50&&(t+=3.5),[t=t/10.5*255,t,t];var r=.5*(1+~~(e>50));return[(1&t)*r*255,(t>>1&1)*r*255,(t>>2&1)*r*255]},i.ansi256.rgb=function(e){if(e>=232){var t=10*(e-232)+8;return[t,t,t]}var r;return e-=16,[Math.floor(e/36)/5*255,Math.floor((r=e%36)/6)/5*255,r%6/5*255]},i.rgb.hex=function(e){var t=(((255&Math.round(e[0]))<<16)+((255&Math.round(e[1]))<<8)+(255&Math.round(e[2]))).toString(16).toUpperCase();return"000000".substring(t.length)+t},i.hex.rgb=function(e){var t=e.toString(16).match(/[a-f0-9]{6}|[a-f0-9]{3}/i);if(!t)return[0,0,0];var r=t[0];3===t[0].length&&(r=r.split("").map((function(e){return e+e})).join(""));var n=parseInt(r,16);return[n>>16&255,n>>8&255,255&n]},i.rgb.hcg=function(e){var t,r=e[0]/255,n=e[1]/255,a=e[2]/255,o=Math.max(Math.max(r,n),a),i=Math.min(Math.min(r,n),a),l=o-i;return t=l<=0?0:o===r?(n-a)/l%6:o===n?2+(a-r)/l:4+(r-n)/l+4,t/=6,[360*(t%=1),100*l,100*(l<1?i/(1-l):0)]},i.hsl.hcg=function(e){var t=e[1]/100,r=e[2]/100,n=1,a=0;return(n=r<.5?2*t*r:2*t*(1-r))<1&&(a=(r-.5*n)/(1-n)),[e[0],100*n,100*a]},i.hsv.hcg=function(e){var t=e[1]/100,r=e[2]/100,n=t*r,a=0;return n<1&&(a=(r-n)/(1-n)),[e[0],100*n,100*a]},i.hcg.rgb=function(e){var t=e[0]/360,r=e[1]/100,n=e[2]/100;if(0===r)return[255*n,255*n,255*n];var a,o=[0,0,0],i=t%1*6,l=i%1,s=1-l;switch(Math.floor(i)){case 0:o[0]=1,o[1]=l,o[2]=0;break;case 1:o[0]=s,o[1]=1,o[2]=0;break;case 2:o[0]=0,o[1]=1,o[2]=l;break;case 3:o[0]=0,o[1]=s,o[2]=1;break;case 4:o[0]=l,o[1]=0,o[2]=1;break;default:o[0]=1,o[1]=0,o[2]=s}return a=(1-r)*n,[255*(r*o[0]+a),255*(r*o[1]+a),255*(r*o[2]+a)]},i.hcg.hsv=function(e){var t=e[1]/100,r=t+e[2]/100*(1-t),n=0;return r>0&&(n=t/r),[e[0],100*n,100*r]},i.hcg.hsl=function(e){var t=e[1]/100,r=e[2]/100*(1-t)+.5*t,n=0;return r>0&&r<.5?n=t/(2*r):r>=.5&&r<1&&(n=t/(2*(1-r))),[e[0],100*n,100*r]},i.hcg.hwb=function(e){var t=e[1]/100,r=t+e[2]/100*(1-t);return[e[0],100*(r-t),100*(1-r)]},i.hwb.hcg=function(e){var t=e[1]/100,r=1-e[2]/100,n=r-t,a=0;return n<1&&(a=(r-n)/(1-n)),[e[0],100*n,100*a]},i.apple.rgb=function(e){return[e[0]/65535*255,e[1]/65535*255,e[2]/65535*255]},i.rgb.apple=function(e){return[e[0]/255*65535,e[1]/255*65535,e[2]/255*65535]},i.gray.rgb=function(e){return[e[0]/100*255,e[0]/100*255,e[0]/100*255]},i.gray.hsl=i.gray.hsv=function(e){return[0,0,e[0]]},i.gray.hwb=function(e){return[0,100,e[0]]},i.gray.cmyk=function(e){return[0,0,0,e[0]]},i.gray.lab=function(e){return[e[0],0,0]},i.gray.hex=function(e){var t=255&Math.round(e[0]/100*255),r=((t<<16)+(t<<8)+t).toString(16).toUpperCase();return"000000".substring(r.length)+r},i.rgb.gray=function(e){return[(e[0]+e[1]+e[2])/3/255*100]}},function(e,t,r){var n=r(1),a=r(4),o=Object.hasOwnProperty,i={};for(var l in n)o.call(n,l)&&(i[n[l]]=l);var s=e.exports={to:{},get:{}};function u(e,t,r){return Math.min(Math.max(t,e),r)}function c(e){var t=Math.round(e).toString(16).toUpperCase();return t.length<2?"0"+t:t}s.get=function(e){var t,r;switch(e.substring(0,3).toLowerCase()){case"hsl":t=s.get.hsl(e),r="hsl";break;case"hwb":t=s.get.hwb(e),r="hwb";break;default:t=s.get.rgb(e),r="rgb"}return t?{model:r,value:t}:null},s.get.rgb=function(e){if(!e)return null;var t,r,a,i=[0,0,0,1];if(t=e.match(/^#([a-f0-9]{6})([a-f0-9]{2})?$/i)){for(a=t[2],t=t[1],r=0;r<3;r++){var l=2*r;i[r]=parseInt(t.slice(l,l+2),16)}a&&(i[3]=parseInt(a,16)/255)}else if(t=e.match(/^#([a-f0-9]{3,4})$/i)){for(a=(t=t[1])[3],r=0;r<3;r++)i[r]=parseInt(t[r]+t[r],16);a&&(i[3]=parseInt(a+a,16)/255)}else if(t=e.match(/^rgba?\(\s*([+-]?\d+)(?=[\s,])\s*(?:,\s*)?([+-]?\d+)(?=[\s,])\s*(?:,\s*)?([+-]?\d+)\s*(?:[,|\/]\s*([+-]?[\d\.]+)(%?)\s*)?\)$/)){for(r=0;r<3;r++)i[r]=parseInt(t[r+1],0);t[4]&&(t[5]?i[3]=.01*parseFloat(t[4]):i[3]=parseFloat(t[4]))}else{if(!(t=e.match(/^rgba?\(\s*([+-]?[\d\.]+)\%\s*,?\s*([+-]?[\d\.]+)\%\s*,?\s*([+-]?[\d\.]+)\%\s*(?:[,|\/]\s*([+-]?[\d\.]+)(%?)\s*)?\)$/)))return(t=e.match(/^(\w+)$/))?"transparent"===t[1]?[0,0,0,0]:o.call(n,t[1])?((i=n[t[1]])[3]=1,i):null:null;for(r=0;r<3;r++)i[r]=Math.round(2.55*parseFloat(t[r+1]));t[4]&&(t[5]?i[3]=.01*parseFloat(t[4]):i[3]=parseFloat(t[4]))}for(r=0;r<3;r++)i[r]=u(i[r],0,255);return i[3]=u(i[3],0,1),i},s.get.hsl=function(e){if(!e)return null;var t=e.match(/^hsla?\(\s*([+-]?(?:\d{0,3}\.)?\d+)(?:deg)?\s*,?\s*([+-]?[\d\.]+)%\s*,?\s*([+-]?[\d\.]+)%\s*(?:[,|\/]\s*([+-]?(?=\.\d|\d)(?:0|[1-9]\d*)?(?:\.\d*)?(?:[eE][+-]?\d+)?)\s*)?\)$/);if(t){var r=parseFloat(t[4]);return[(parseFloat(t[1])%360+360)%360,u(parseFloat(t[2]),0,100),u(parseFloat(t[3]),0,100),u(isNaN(r)?1:r,0,1)]}return null},s.get.hwb=function(e){if(!e)return null;var t=e.match(/^hwb\(\s*([+-]?\d{0,3}(?:\.\d+)?)(?:deg)?\s*,\s*([+-]?[\d\.]+)%\s*,\s*([+-]?[\d\.]+)%\s*(?:,\s*([+-]?(?=\.\d|\d)(?:0|[1-9]\d*)?(?:\.\d*)?(?:[eE][+-]?\d+)?)\s*)?\)$/);if(t){var r=parseFloat(t[4]);return[(parseFloat(t[1])%360+360)%360,u(parseFloat(t[2]),0,100),u(parseFloat(t[3]),0,100),u(isNaN(r)?1:r,0,1)]}return null},s.to.hex=function(){var e=a(arguments);return"#"+c(e[0])+c(e[1])+c(e[2])+(e[3]<1?c(Math.round(255*e[3])):"")},s.to.rgb=function(){var e=a(arguments);return e.length<4||1===e[3]?"rgb("+Math.round(e[0])+", "+Math.round(e[1])+", "+Math.round(e[2])+")":"rgba("+Math.round(e[0])+", "+Math.round(e[1])+", "+Math.round(e[2])+", "+e[3]+")"},s.to.rgb.percent=function(){var e=a(arguments),t=Math.round(e[0]/255*100),r=Math.round(e[1]/255*100),n=Math.round(e[2]/255*100);return e.length<4||1===e[3]?"rgb("+t+"%, "+r+"%, "+n+"%)":"rgba("+t+"%, "+r+"%, "+n+"%, "+e[3]+")"},s.to.hsl=function(){var e=a(arguments);return e.length<4||1===e[3]?"hsl("+e[0]+", "+e[1]+"%, "+e[2]+"%)":"hsla("+e[0]+", "+e[1]+"%, "+e[2]+"%, "+e[3]+")"},s.to.hwb=function(){var e=a(arguments),t="";return e.length>=4&&1!==e[3]&&(t=", "+e[3]),"hwb("+e[0]+", "+e[1]+"%, "+e[2]+"%"+t+")"},s.to.keyword=function(e){return i[e.slice(0,3)]}},function(e,t,r){"use strict";var n=r(5),a=Array.prototype.concat,o=Array.prototype.slice,i=e.exports=function(e){for(var t=[],r=0,i=e.length;r<i;r++){var l=e[r];n(l)?t=a.call(t,o.call(l)):t.push(l)}return t};i.wrap=function(e){return function(){return e(i(arguments))}}},function(e,t){e.exports=function(e){return!(!e||"string"==typeof e)&&(e instanceof Array||Array.isArray(e)||e.length>=0&&(e.splice instanceof Function||Object.getOwnPropertyDescriptor(e,e.length-1)&&"String"!==e.constructor.name))}},function(e,t,r){var n=r(2),a=r(8),o={};Object.keys(n).forEach((function(e){o[e]={},Object.defineProperty(o[e],"channels",{value:n[e].channels}),Object.defineProperty(o[e],"labels",{value:n[e].labels});var t=a(e);Object.keys(t).forEach((function(r){var n=t[r];o[e][r]=function(e){var t=function(t){if(null==t)return t;arguments.length>1&&(t=Array.prototype.slice.call(arguments));var r=e(t);if("object"==typeof r)for(var n=r.length,a=0;a<n;a++)r[a]=Math.round(r[a]);return r};return"conversion"in e&&(t.conversion=e.conversion),t}(n),o[e][r].raw=function(e){var t=function(t){return null==t?t:(arguments.length>1&&(t=Array.prototype.slice.call(arguments)),e(t))};return"conversion"in e&&(t.conversion=e.conversion),t}(n)}))})),e.exports=o},function(e,t,r){"use strict";e.exports={aliceblue:[240,248,255],antiquewhite:[250,235,215],aqua:[0,255,255],aquamarine:[127,255,212],azure:[240,255,255],beige:[245,245,220],bisque:[255,228,196],black:[0,0,0],blanchedalmond:[255,235,205],blue:[0,0,255],blueviolet:[138,43,226],brown:[165,42,42],burlywood:[222,184,135],cadetblue:[95,158,160],chartreuse:[127,255,0],chocolate:[210,105,30],coral:[255,127,80],cornflowerblue:[100,149,237],cornsilk:[255,248,220],crimson:[220,20,60],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgoldenrod:[184,134,11],darkgray:[169,169,169],darkgreen:[0,100,0],darkgrey:[169,169,169],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkseagreen:[143,188,143],darkslateblue:[72,61,139],darkslategray:[47,79,79],darkslategrey:[47,79,79],darkturquoise:[0,206,209],darkviolet:[148,0,211],deeppink:[255,20,147],deepskyblue:[0,191,255],dimgray:[105,105,105],dimgrey:[105,105,105],dodgerblue:[30,144,255],firebrick:[178,34,34],floralwhite:[255,250,240],forestgreen:[34,139,34],fuchsia:[255,0,255],gainsboro:[220,220,220],ghostwhite:[248,248,255],gold:[255,215,0],goldenrod:[218,165,32],gray:[128,128,128],green:[0,128,0],greenyellow:[173,255,47],grey:[128,128,128],honeydew:[240,255,240],hotpink:[255,105,180],indianred:[205,92,92],indigo:[75,0,130],ivory:[255,255,240],khaki:[240,230,140],lavender:[230,230,250],lavenderblush:[255,240,245],lawngreen:[124,252,0],lemonchiffon:[255,250,205],lightblue:[173,216,230],lightcoral:[240,128,128],lightcyan:[224,255,255],lightgoldenrodyellow:[250,250,210],lightgray:[211,211,211],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightsalmon:[255,160,122],lightseagreen:[32,178,170],lightskyblue:[135,206,250],lightslategray:[119,136,153],lightslategrey:[119,136,153],lightsteelblue:[176,196,222],lightyellow:[255,255,224],lime:[0,255,0],limegreen:[50,205,50],linen:[250,240,230],magenta:[255,0,255],maroon:[128,0,0],mediumaquamarine:[102,205,170],mediumblue:[0,0,205],mediumorchid:[186,85,211],mediumpurple:[147,112,219],mediumseagreen:[60,179,113],mediumslateblue:[123,104,238],mediumspringgreen:[0,250,154],mediumturquoise:[72,209,204],mediumvioletred:[199,21,133],midnightblue:[25,25,112],mintcream:[245,255,250],mistyrose:[255,228,225],moccasin:[255,228,181],navajowhite:[255,222,173],navy:[0,0,128],oldlace:[253,245,230],olive:[128,128,0],olivedrab:[107,142,35],orange:[255,165,0],orangered:[255,69,0],orchid:[218,112,214],palegoldenrod:[238,232,170],palegreen:[152,251,152],paleturquoise:[175,238,238],palevioletred:[219,112,147],papayawhip:[255,239,213],peachpuff:[255,218,185],peru:[205,133,63],pink:[255,192,203],plum:[221,160,221],powderblue:[176,224,230],purple:[128,0,128],rebeccapurple:[102,51,153],red:[255,0,0],rosybrown:[188,143,143],royalblue:[65,105,225],saddlebrown:[139,69,19],salmon:[250,128,114],sandybrown:[244,164,96],seagreen:[46,139,87],seashell:[255,245,238],sienna:[160,82,45],silver:[192,192,192],skyblue:[135,206,235],slateblue:[106,90,205],slategray:[112,128,144],slategrey:[112,128,144],snow:[255,250,250],springgreen:[0,255,127],steelblue:[70,130,180],tan:[210,180,140],teal:[0,128,128],thistle:[216,191,216],tomato:[255,99,71],turquoise:[64,224,208],violet:[238,130,238],wheat:[245,222,179],white:[255,255,255],whitesmoke:[245,245,245],yellow:[255,255,0],yellowgreen:[154,205,50]}},function(e,t,r){var n=r(2);function a(e){var t=function(){for(var e={},t=Object.keys(n),r=t.length,a=0;a<r;a++)e[t[a]]={distance:-1,parent:null};return e}(),r=[e];for(t[e].distance=0;r.length;)for(var a=r.pop(),o=Object.keys(n[a]),i=o.length,l=0;l<i;l++){var s=o[l],u=t[s];-1===u.distance&&(u.distance=t[a].distance+1,u.parent=a,r.unshift(s))}return t}function o(e,t){return function(r){return t(e(r))}}function i(e,t){for(var r=[t[e].parent,e],a=n[t[e].parent][e],i=t[e].parent;t[i].parent;)r.unshift(t[i].parent),a=o(n[t[i].parent][i],a),i=t[i].parent;return a.conversion=r,a}e.exports=function(e){for(var t=a(e),r={},n=Object.keys(t),o=n.length,l=0;l<o;l++){var s=n[l];null!==t[s].parent&&(r[s]=i(s,t))}return r}},function(e,t,r){"use strict";r.r(t),r.d(t,"run",(function(){return ve})),r.d(t,"init",(function(){return ke})),r.d(t,"convertBg",(function(){return we})),r.d(t,"extend",(function(){return xe})),r.d(t,"updateStyle",(function(){return Me}));var n="(prefers-color-scheme: dark)",a="data_color_scheme_dark",o="".concat(1*new Date).concat(Math.round(10*Math.random())),i="data-darkmode-color-".concat(o),l="data-darkmode-bgcolor-".concat(o),s="data-darkmode-original-color-".concat(o),u="data-darkmode-original-bgcolor-".concat(o),c="data-darkmode-bgimage-".concat(o),h=window.getInnerHeight&&window.getInnerHeight()||window.innerHeight||document.documentElement.clientHeight,f=["TABLE","TR","TD","TH"],d=/ !important$/,g={hasInit:!1,begin:null,showFirstPage:null,error:null,mode:"",whitelist:{tagName:["MPCPS","IFRAME"]},needJudgeFirstPage:!0,delayBgJudge:!1,container:null,cssSelectorsPrefix:"",defaultLightTextColor:"#191919",defaultLightBgColor:"#fff",defaultDarkTextColor:"#a3a3a3",defaultDarkBgColor:"#191919",set:function(e,t,r){var n=t[r];switch(e){case"boolean":"boolean"==typeof n&&(this[r]=n);break;case"string":"string"==typeof n&&""!==n&&(this[r]=n);break;case"function":"function"==typeof n&&(this[r]=n);break;case"dom":n instanceof HTMLElement&&(this[r]=n)}}};function b(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function p(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function y(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function m(e,t,r){return t&&y(e.prototype,t),r&&y(e,r),Object.defineProperty(e,"prototype",{writable:!1}),e}var v=[],k=[],w=function(){function e(){p(this,e)}return m(e,[{key:"loopTimes",get:function(){return ce.loopTimes}},{key:"isDarkmode",get:function(){return be.isDarkmode}},{key:"addCss",value:function(e,t){var r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];(r?v:k).push(de.genCss(e,t.map((function(e){var t=e.key,r=e.value;return de.genCssKV(t,r)})).join("")))}}]),e}(),x=function(){function e(){p(this,e),b(this,"_plugins",[]),b(this,"length",0),b(this,"loopTimes",0),b(this,"firstPageStyle",""),b(this,"otherPageStyle",""),b(this,"firstPageStyleNoMQ",""),b(this,"otherPageStyleNoMQ","")}return m(e,[{key:"extend",value:function(e){this._plugins.push(new(e(w))),this.length++}},{key:"emit",value:function(e){for(var t=arguments.length,r=new Array(t>1?t-1:0),n=1;n<t;n++)r[n-1]=arguments[n];this._plugins.forEach((function(t){"function"==typeof t[e]&&t[e].apply(t,r)}))}},{key:"addCss",value:function(e){e?(this.firstPageStyle+=v.join(""),this.firstPageStyleNoMQ+=k.join("")):(this.otherPageStyle+=v.join(""),this.otherPageStyleNoMQ+=k.join(""))}},{key:"resetCss",value:function(){v=[],k=[]}}]),e}();function M(e){return(M="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function _(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function C(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var j=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),C(this,"_queue",[]),C(this,"_idx",0),this._prefix=t}var t,r,n;return t=e,(r=[{key:"push",value:function(e){var t="".concat(this._prefix).concat(this._idx++);e.classList.add(t),this._queue.push({el:e,className:t,updated:!g.delayBgJudge})}},{key:"forEach",value:function(e){var t=[];for(this._queue.forEach((function(r,n){r.updated&&(t.unshift(n),M(e)&&e(r.el))}));t.length;)this._queue.splice(t.shift(),1)}},{key:"update",value:function(e){this._queue.forEach((function(t){t.updated||Array.prototype.some.call(e,(function(e){return!(1!==e.nodeType||!e.classList.contains(t.className)||(t.el=e,t.updated=!0,0))}))}))}}])&&_(t.prototype,r),n&&_(t,n),Object.defineProperty(t,"prototype",{writable:!1}),e}();function S(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function P(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var O=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),P(this,"_stack",[]),P(this,"_idx",0),this._prefix=t,this.classNameReg=new RegExp("".concat(this._prefix,"\\d+"))}var t,r,n;return t=e,(r=[{key:"push",value:function(e,t){var r="".concat(this._prefix).concat(this._idx++);e.classList.add(r),this._stack.unshift({el:e,className:r,cssKV:t,updated:!g.delayBgJudge})}},{key:"contains",value:function(e,t){var r=e.getBoundingClientRect(),n=[];for(this._stack.forEach((function(e,t){if(e.updated){e.rect||(e.rect=e.el.getBoundingClientRect());var a=e.rect;r.top>=a.bottom||r.bottom<=a.top||r.left>=a.right||r.right<=a.left||n.unshift(t)}}));n.length;){var a=this._stack.splice(n.shift(),1)[0];"function"==typeof t&&t(a)}}},{key:"update",value:function(e){this._stack.forEach((function(t){t.updated||Array.prototype.some.call(e,(function(e){return!(1!==e.nodeType||!e.classList.contains(t.className)||(t.el=e,t.updated=!0,0))}))}))}}])&&S(t.prototype,r),n&&S(t,n),Object.defineProperty(t,"prototype",{writable:!1}),e}();function B(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,o=[],i=!0,l=!1;try{for(r=r.call(e);!(i=(n=r.next()).done)&&(o.push(n.value),!t||o.length!==t);i=!0);}catch(e){l=!0,a=e}finally{try{i||null==r.return||r.return()}finally{if(l)throw a}}return o}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return A(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return A(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function A(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function N(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function E(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var T=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),E(this,"_firstPageStyle",""),E(this,"_otherPageStyle",""),E(this,"isFinish",!1)}var t,r,o;return t=e,(r=[{key:"genCssKV",value:function(e,t){return"".concat(e,": ").concat(t," !important;")}},{key:"genCss",value:function(e,t){return"".concat("dark"===g.mode?"html.".concat(a," "):"").concat(g.cssSelectorsPrefix&&"".concat(g.cssSelectorsPrefix," "),".").concat(e,"{").concat(t,"}")}},{key:"addCss",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];this[t?"_firstPageStyle":"_otherPageStyle"]+=e,ce.addCss(t)}},{key:"writeStyle",value:function(){var e=arguments.length>0&&void 0!==arguments[0]&&arguments[0];!e&&be.isDarkmode&&(this.isFinish=!0);var t=(be.isDarkmode?[{target:this,key:["_firstPageStyle","_otherPageStyle"],needMediaQuery:!0}]:[]).concat([{target:ce,key:["firstPageStyle","otherPageStyle"],needMediaQuery:!0},{target:ce,key:["firstPageStyleNoMQ","otherPageStyleNoMQ"],needMediaQuery:!1}]).map((function(t){var r=t.target,a=B(t.key,2),o=a[0],i=a[1],l=t.needMediaQuery,s="";e?s=o:(r[i]=r[o]+r[i],r[o]="",s=i);var u=r[s];return u?(r[s]="","dark"!==g.mode&&l?"@media ".concat(n," {").concat(u,"}"):u):""})).join("");t&&document.head.insertAdjacentHTML("beforeend",'<style type="text/css">'.concat(t,"</style>"))}}])&&N(t.prototype,r),o&&N(t,o),Object.defineProperty(t,"prototype",{writable:!1}),e}();function F(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function D(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function L(e){return function(e){if(Array.isArray(e))return I(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||function(e,t){if(!e)return;if("string"==typeof e)return I(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return I(e,t)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function I(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function q(e){var t;return(t=[e]).concat.apply(t,L(e.querySelectorAll("*")))}var $={"ue-table-interlace-color-single":"#fcfcfc","ue-table-interlace-color-double":"#f7faff"};var V=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),D(this,"_nodes",[]),D(this,"_firstPageNodes",[]),D(this,"_delayNodes",[]),D(this,"showFirstPage",!1)}var t,r,n;return t=e,(r=[{key:"length",get:function(){return this._nodes.length}},{key:"set",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this._nodes=e}},{key:"get",value:function(){var e=[];return this._nodes.length?(e=this._nodes,be.isDarkmode&&(this._nodes=[])):this._delayNodes.length?(e=this._delayNodes,this._delayNodes=[]):g.container&&(e=g.container.querySelectorAll("*")),e}},{key:"delay",value:function(){var e=this;Array.prototype.forEach.call(this._nodes,(function(t){return e._delayNodes.push(t)})),this._nodes=[]}},{key:"hasDelay",value:function(){return this._delayNodes.length>0}},{key:"addFirstPageNode",value:function(e){this._firstPageNodes.push(e)}},{key:"showFirstPageNodes",value:function(){this._firstPageNodes.forEach((function(e){return e.style.visibility="visible"})),this.showFirstPage=!0}},{key:"emptyFirstPageNodes",value:function(){this._firstPageNodes=[]}}])&&F(t.prototype,r),n&&F(t,n),Object.defineProperty(t,"prototype",{writable:!1}),e}(),z=r(0),K=r.n(z),J=r(1),R=r.n(J);function U(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,o=[],i=!0,l=!1;try{for(r=r.call(e);!(i=(n=r.next()).done)&&(o.push(n.value),!t||o.length!==t);i=!0);}catch(e){l=!0,a=e}finally{try{i||null==r.return||r.return()}finally{if(l)throw a}}return o}(e,t)||Q(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function H(e){return function(e){if(Array.isArray(e))return G(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||Q(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function Q(e,t){if(e){if("string"==typeof e)return G(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?G(e,t):void 0}}function G(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function W(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function X(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}R.a.windowtext=[0,0,0],R.a.transparent=[255,255,255,0];var Y=/<\$#_SEMICOLON_#\$>/g,Z=new RegExp("".concat("js_darkmode__","\\d+")),ee=new RegExp(Object.keys(R.a).map((function(e){return"\\b".concat(e,"\\b")})).join("|"),"ig"),te=/\brgba?\([^)]+\)/i,re=/\brgba?\([^)]+\)/gi,ne=function(e){return e.replace(d,"")},ae=function(e,t){return ne(e).replace(ee,(function(e){if(!t&&"transparent"===e)return e;var r=R.a[e.toLowerCase()];return"".concat(r.length>3?"rgba":"rgb","(").concat(r.toString(),")")}))},oe=function(e){if(!e||e.length<1)return"";if(1===e.length)return e[0];for(var t=e.shift(),r=e.shift();r;){var n=K()(r);t=K()(t).mix(n,n.alpha()),r=e.shift()}return t},ie=function(e){var t=ae(e);return te.test(t)?t:""},le=function(e){return(299*e[0]+587*e[1]+114*e[2])/1e3},se=function(e,t){var r=e/le(t),n=Math.min(255,t[0]*r),a=Math.min(255,t[1]*r),o=Math.min(255,t[2]*r);return 0===a||255===n||255===o?a=(1e3*e-299*n-114*o)/587:0===n?n=(1e3*e-587*a-114*o)/299:0!==o&&255!==a||(o=(1e3*e-299*n-587*a)/114),K.a.rgb(n,a,o)},ue=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),X(this,"_idx",0),X(this,"_defaultDarkTextColorRgb",K()(g.defaultDarkTextColor).rgb().array()),X(this,"_defaultDarkBgColorRgb",K()(g.defaultDarkBgColor).rgb().array()),X(this,"_defaultDarkBgColorHSL",K()(g.defaultDarkBgColor).hsl().array()),X(this,"_defaultDarkTextColorBrightness",le(this._defaultDarkTextColorRgb)),X(this,"_defaultDarkBgColorBrightness",le(this._defaultDarkBgColorRgb)),X(this,"_defaultDarkBgColorHslBrightness",this._defaultDarkBgColorHSL[2]),X(this,"_maxLimitOffsetBrightness",this._defaultDarkTextColorBrightness-this._defaultDarkBgColorBrightness),X(this,"isDarkmode",!1)}var t,r,n;return t=e,(r=[{key:"_adjustTextBrightness",value:function(e,t){var r=t.rgb().array(),n=t.alpha(),a=le(r)*n+this._defaultDarkBgColorBrightness*(1-n),o=e.rgb().array(),i=e.hsl().array(),l=e.alpha(),s=le(o),u=Math.abs(a-s);if(s>=250)return e;if(u>this._maxLimitOffsetBrightness&&a<=this._defaultDarkBgColorBrightness+2)return se(this._maxLimitOffsetBrightness+a,o).alpha(l);if(u>=65)return e;if(a>=100){if(i[2]>50){i[2]=90-i[2];var c=K.a.hsl.apply(K.a,H(i)).alpha(l);return this._adjustTextBrightness(c,t)}return se(Math.min(this._maxLimitOffsetBrightness,a-65),o).alpha(l)}if(i[2]<=40){i[2]=90-i[2];var h=K.a.hsl.apply(K.a,H(i)).alpha(l);return this._adjustTextBrightness(h,t)}return se(Math.min(this._maxLimitOffsetBrightness,a+65),o).alpha(l)}},{key:"_adjustBackgroundBrightness",value:function(e){var t=e.rgb().array(),r=e.hsl().array(),n=e.alpha(),a=le(t),o=e;return 0===r[1]&&r[2]>40||a>250?o=K.a.hsl(0,0,Math.min(100,100+this._defaultDarkBgColorHslBrightness-r[2])):a>190?o=se(190,t).alpha(n):r[2]<22&&(r[2]=22,o=K.a.hsl.apply(K.a,H(r))),o.alpha(n).rgb()}},{key:"_adjustBrightness",value:function(e,t,r,n){var a,o=e.alpha(),s="";if(r.isBgColor){if(t[c]&&o>=.05&&delete t[c],a=this._adjustBackgroundBrightness(e),!r.hasInlineColor){var u=t[i]||g.defaultLightTextColor,h=a||e,f=this._adjustBrightness(K()(u),t,{isTextColor:!0,parentElementBgColorStr:h},n);f.newColor?s+=de.genCssKV("color",f.newColor):s+=de.genCssKV("color",u)}}else if(r.isTextColor||r.isBorderColor){var d=r.parentElementBgColorStr||r.isTextColor&&t[l]||g.defaultDarkBgColor,b=K()(d);t[c]||(a=this._adjustTextBrightness(e,b),ce.emit("afterConvertTextColor".concat(n?"ByUpdateStyle":""),t,{fontColor:a,bgColor:b}))}else r.isTextShadow&&(t[c]||(a=this._adjustBackgroundBrightness(e)));return{newColor:a&&e.toString()!==a.toString()&&a.alpha(o).rgb(),extStyle:s}}},{key:"_try",value:function(e){try{return e()}catch(e){console.log("An error occurred when running the dark mode conversion algorithm\n",e),"function"==typeof g.error&&g.error(e)}}},{key:"convert",value:function(e,t,r){var n=this;ce.resetCss(),ce.emit("beforeConvertNode".concat(r?"ByUpdateStyle":""),e);var a,o,h="",b="";if(this.isDarkmode||r){var p=e.nodeName;if(g.whitelist.tagName.indexOf(p)>-1)return"";var y=e.style;t||(t=(y.cssText&&y.cssText.replace(/("[^;]*);([^;]*")|('[^;]*);([^;]*')/g,"$1$3".concat("<$#_SEMICOLON_#$>","$2$4")).split(";")||[]).map((function(e){var t=e.indexOf(":");return[e.slice(0,t).toLowerCase(),e.slice(t+1).replace(Y,";")].map((function(e){return(e||"").replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"")}))})));var m,v,k=!1,w=!1,x=!1;t=t.filter((function(e){var t=U(e,2),r=t[0],n=t[1];return"color"===r?k=!0:/background/i.test(r)&&(w=!0,"background-position"===r?m=n:"background-size"===r&&(v=n)),(/background/i.test(r)||/^(-webkit-)?border-image/.test(r))&&/url\([^)]*\)/i.test(n)&&(x=!0),["-webkit-border-image","border-image","color","background-color","background-image","background","border","border-top","border-right","border-bottom","border-left","border-color","border-top-color","border-right-color","border-bottom-color","border-left-color","-webkit-text-fill-color","-webkit-text-stroke","-webkit-text-stroke-color","text-shadow"].indexOf(r)>-1})).sort((function(e,t){var r=U(e,1)[0],n=U(t,1)[0];return"color"===r||"background-image"===r&&"background-color"===n||0===n.indexOf("-webkit-text")?1:-1})),f.indexOf(p)>-1&&!w&&this._try((function(){var r=function(e){var t=null;return Array.prototype.some.call(e.classList,(function(e){return!!$[e]&&(t=$[e],!0)})),t}(e);r||(r=e.getAttribute("bgcolor")),r&&(t.unshift(["background-color",K()(r).toString()]),w=!0)})),"FONT"!==p||k||this._try((function(){var r=e.getAttribute("color");r&&(t.push(["color",K()(r).toString()]),k=!0)}));var M="",_="",C=0;t.some((function(e,t){var r=U(e,2),a=r[0],o=r[1];return n._try((function(){if(0!==a.indexOf("-webkit-text"))return C=t,!0;switch(a){case"-webkit-text-fill-color":M=ie(o);break;case"-webkit-text-stroke":var e=o.split(" ");2===e.length&&(_=ie(e[1]));break;case"-webkit-text-stroke-color":_=ie(o)}return!1}))})),M&&(k?t[t.length-1]=["-webkit-text-fill-color",M]:(t.push(["-webkit-text-fill-color",M]),k=!0)),C&&(t.splice(0,C),_&&t.unshift(["-webkit-text-stroke-color",_]));var j="",S="";if(r&&e.className&&"string"==typeof e.className){var P=e.className.match(Z);P&&(j=P[0]),(P=e.className.match(fe.classNameReg))&&(S=P[0])}var O="";t.forEach((function(t){var a=U(t,2),o=a[0],h=a[1];return n._try((function(){var t,a=h,f=!1,p=/^background/.test(o),M="text-shadow"===o,_=["-webkit-text-stroke-color","color","-webkit-text-fill-color"].indexOf(o),C=/^border/.test(o),j=/gradient/.test(h),P=[],B="";if(h=ae(h,j),te.test(h)){if(j){for(var A=re.exec(h);A;)P.push(A[0]),A=re.exec(h);t=oe(P)}var N=0;h=h.replace(re,(function(a){j&&(a=t,f=!0);var o=n._adjustBrightness(K()(a),e,{isBgColor:p,isTextShadow:M,isTextColor:_>-1,isBorderColor:C,hasInlineColor:k},r),h=!x&&o.newColor;if(B+=o.extStyle,p||_>0){var d=p?l:i,b=p?u:s,y=h?h.toString():a;0===N&&q(e).forEach((function(e){var t=e[b]||g.defaultLightBgColor;e[d]=y,e[b]=t.split("|").concat(a).join("|"),p&&K()(y).alpha()>=.05&&e[c]&&delete e[c]}))}return h&&(f=!0),N+=1,h||a})).replace(/\s?!\s?important/gi,"")}if(B&&(O+=B),!(e instanceof SVGElement)){var E=/^background/.test(o),T=/^(-webkit-)?border-image/.test(o);if((E||T)&&/url\([^)]*\)/i.test(h)){f=!0;var F=oe((e[u]||g.defaultLightBgColor).split("|"));if(h=h.replace(/^(.*?)url\(([^)]*)\)(.*)$/i,(function(t){var r=t,n="",a="",i="";return e[c]||q(e).forEach((function(e){e[c]=!0})),E?(r="linear-gradient(".concat("rgba(0,0,0,0.2)",", ").concat("rgba(0,0,0,0.2)","),").concat(t),i=de.genCssKV(o,"".concat(r,",linear-gradient(").concat(F,", ").concat(F,")")),m&&(n="top left,".concat(m),O+=de.genCssKV("background-position","".concat(n)),i+=de.genCssKV("background-position","".concat(n,",top left"))),v&&(a="100%,".concat(v),O+=de.genCssKV("background-size","".concat(a)),i+=de.genCssKV("background-size","".concat(a,",100%"))),S?b+=de.genCss(S,i):fe.push(e,i)):w||(i=de.genCssKV("background-image","linear-gradient(".concat("rgba(0,0,0,0.2)",", ").concat("rgba(0,0,0,0.2)","),linear-gradient(").concat(F,", ").concat(F,")")),S?b+=de.genCss(S,i):fe.push(e,i)),r})),!k){var D=oe((e[s]||g.defaultLightTextColor).split("|"));O+=de.genCssKV("color",D),q(e).forEach((function(e){e[i]=D}))}}}f&&(!r&&d.test(a)&&(y[o]=ne(a)),j?S?b+=de.genCss(S,de.genCssKV(o,h)):fe.push(e,de.genCssKV(o,h)):O+=de.genCssKV(o,h))}))})),O&&(e.setAttribute("data-style",y.cssText),j||(j="".concat("js_darkmode__").concat(this._idx++),e.classList.add(j)),h+=O?de.genCss(j,O):""),h+=b,!r&&(a=e,o="",Array.prototype.forEach.call(a.childNodes,(function(e){3===e.nodeType&&(o+=e.nodeValue.replace(/\s/g,""))})),o.length>0)&&(g.delayBgJudge?he.push(e):fe.contains(e,(function(e){h+=de.genCss(e.className,e.cssKV)})))}return ce.emit("afterConvertNode".concat(r?"ByUpdateStyle":""),e),h}}])&&W(t.prototype,r),n&&W(t,n),Object.defineProperty(t,"prototype",{writable:!1}),e}(),ce=new x,he=new j("".concat("js_darkmode__","text__")),fe=new O("".concat("js_darkmode__","bg__")),de=new T,ge=new V,be=new ue,pe=new RegExp("".concat("js_darkmode__","[^ ]+"),"g"),ye=null,me=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{type:"dom"};if(t.force&&(de.isFinish=!1),!de.isFinish)try{be.isDarkmode=g.mode?"dark"===g.mode:e.matches,"dom"===t.type?(be.isDarkmode&&"function"==typeof g.begin&&g.begin(ge.hasDelay()),Array.prototype.forEach.call(ge.get(),(function(e){if(be.isDarkmode&&e.className&&"string"==typeof e.className&&(e.className=e.className.replace(pe,"")),be.isDarkmode||ce.length)if(g.needJudgeFirstPage){var t=e.getBoundingClientRect(),r=t.top,n=t.bottom;r<=0&&n<=0?de.addCss(be.convert(e)):r>0&&r<h||n>0&&n<h?(ge.addFirstPageNode(e),de.addCss(be.convert(e),!0)):(g.needJudgeFirstPage=!1,de.writeStyle(!0),ge.showFirstPageNodes(),"function"==typeof g.showFirstPage&&g.showFirstPage(),de.addCss(be.convert(e)))}else de.addCss(be.convert(e))})),ce.loopTimes++):"bg"===t.type&&be.isDarkmode&&he.forEach((function(e){return fe.contains(e,(function(e){de.addCss(de.genCss(e.className,e.cssKV))}))})),(g.needJudgeFirstPage||!g.needJudgeFirstPage&&!ge.showFirstPage)&&"function"==typeof g.showFirstPage&&g.showFirstPage(),de.writeStyle(),ge.emptyFirstPageNodes(),be.isDarkmode||(g.needJudgeFirstPage=!1,g.delayBgJudge=!1,null===g.container&&"dom"===t.type&&ge.length&&ge.delay())}catch(e){console.log("An error occurred when running the dark mode conversion algorithm\n",e),"function"==typeof g.error&&g.error(e)}};function ve(e,t){ke(t),ge.set(e),me(ye,{force:!0,type:"dom"})}function ke(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};if(!g.hasInit){g.hasInit=!0;var t=g.whitelist.tagName;e.whitelist&&e.whitelist.tagName instanceof Array&&e.whitelist.tagName.forEach((function(e){e=e.toUpperCase(),-1===t.indexOf(e)&&t.push(e)})),["dark","light"].indexOf(e.mode)>-1&&(g.set("string",e,"mode"),document.getElementsByTagName("html")[0].classList.add(a)),g.set("function",e,"begin"),g.set("function",e,"showFirstPage"),g.set("function",e,"error"),g.set("boolean",e,"needJudgeFirstPage"),g.set("boolean",e,"delayBgJudge"),g.set("dom",e,"container"),g.set("string",e,"cssSelectorsPrefix"),g.set("string",e,"defaultLightTextColor"),g.set("string",e,"defaultLightBgColor"),g.set("string",e,"defaultDarkTextColor"),g.set("string",e,"defaultDarkBgColor"),!g.mode&&null===ye&&window.matchMedia&&(ye=window.matchMedia(n)).addListener(me)}}function we(e){ge.set(e),null!==g.container&&(fe.update(e),he.update(e)),me(ye,{force:!0,type:"bg"})}function xe(e){e.forEach((function(e){return ce.extend(e)}))}function Me(e,t){de.isFinish&&(de.addCss(be.convert(e,t?Object.keys(t).map((function(e){return[e,t[e]]})):void 0,!0),!1),de.writeStyle())}}])}));</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>!function(){"use strict";var t=window.WebKitMutationObserver||window.MutationObserver||window.MozMutationObserver,e=0===location.href.indexOf("http://"),r=function(t){if(t){var e=t.match(/http(?:s)?:\/\/([^\/]+?)(\/|$)/);if(e&&!/qq\.com(\:8080)?$/.test(e[1])&&!/weishi\.com$/.test(e[1]))return!0}return!1};-1===location.href.indexOf("safe=0")&&e&&"function"==typeof t&&"mp.weixin.qq.com"===location.host&&(window.__observer_data={count:0,exec_time:0,list:[]},window.__observer=new t((function(t){window.__observer_data.count++;var e=new Date,o=[];t.forEach((function(t){for(var e=t.addedNodes,n=0;n<e.length;n++){var i=e[n];if("SCRIPT"===i.tagName){var _=i.src;r(_)&&(window.__observer_data.list.push(_),o.push(i)),!_&&window.__nonce_str&&i.getAttribute("nonce")!=window.__nonce_str&&(window.__observer_data.list.push("inlinescript_without_nonce"),o.push(i))}}}));for(var n=0;n<o.length;n++){var i=o[n];i.parentNode&&i.parentNode.removeChild(i)}window.__observer_data.exec_time+=new Date-e})),window.__observer.observe(document,{subtree:!0,childList:!0})),function(){if(-1===location.href.indexOf("safe=0")&&Math.random()<.01&&e&&HTMLScriptElement.prototype.__lookupSetter__&&void 0!==Object.defineProperty){window.__danger_src={xmlhttprequest:[],script_src:[],script_setAttribute:[]};var t="$"+Math.random(),o="Setter__";HTMLScriptElement.prototype.__old_method_script_src=HTMLScriptElement.prototype["__lookup"+o]("src"),HTMLScriptElement.prototype["__define"+o]("src",(function(t){t&&r(t)&&window.__danger_src.script_src.push(t),this.__old_method_script_src(t)}));var n="__setAttribute"+t;Object.defineProperty(Element.prototype,n,{value:Element.prototype.setAttribute,enumerable:!1}),Element.prototype.setAttribute=function(t,e){"SCRIPT"===this.tagName&&"src"===t&&r(e)&&window.__danger_src.script_setAttribute.push(e),this[n](t,e)}}}()}();</script>

    
<script type="module" nonce="1682091926" reportloaderror>!function(){try{new Function("m","return import(m)")}catch(o){console.warn("vite: loading legacy build because dynamic import is unsupported, syntax error above should be ignored");var e=document.getElementById("vite-legacy-polyfill"),n=document.createElement("script");n.src=e.src,n.onload=function(){System.import(document.getElementById('vite-legacy-entry').getAttribute('data-src'))},document.body.appendChild(n)}}();</script>
<script type="module" crossorigin src="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/appmsg.lfxjo50s63acf705.js" nonce="1682091926" reportloaderror></script>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/modulepreload-polyfill.lfxjo50s20934d53.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/preload-helper.lfxjo50s75cca8c9.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/event.lfxjo50sc0ec7339.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/tmpl.lfxjo50s30bd536b.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/core.lfxjo50s5037c32d.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/device.lfxjo50sfc61b246.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/comm_report.lfxjo50s05752e39.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/comm_utils.lfxjo50sb3ef3921.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/page_utils.lfxjo50s33981d02.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/appmsgext.lfxjo50sac78a86a.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/vueComponentNormalizer.lfxjo50sdc678741.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/index.lfxjo50s2f9a5358.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/weui_a11y.lfxjo50s3a8055d0.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/wxwork_hidden.lfxjo50s83c646bb.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/loadscript.lfxjo50s773a7596.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/voice_component.lfxjo50s1c9ecbb4.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/outer_link.lfxjo50sf5e30f24.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/dom.lfxjo50sbbf73dba.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/review_image.lfxjo50s939d9b94.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/set_article_read.lfxjo50s087cfd6b.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/background_color.lfxjo50s09595dc0.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/moment.lfxjo50s1e8ec291.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/like_and_share.lfxjo50sbe65c497.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/controller.lfxjo50s7bb44109.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/see_more.lfxjo50s98b19751.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/modal.lfxjo50s65c91c63.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/intersection-observer.lfxjo50s6dd54785.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/range_close.lfxjo50s3cd1c04f.js" reportloaderror>
<link rel="modulepreload" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/_commonjsHelpers.lfxjo50s03ef80d6.js" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/index.lfxjo50s5c8cdca7.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/weui_a11y.lfxjo50s4586b1a0.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/wxwork_hidden.lfxjo50s9597bd7f.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/see_more.lfxjo50s3d89d3d2.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/controller.lfxjo50s583250e9.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/appmsg.lfxjo50s68079f33.css" reportloaderror>
<link rel="stylesheet" href="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/tencent_portfolio_light.lfxjo50sb73a2535.css" reportloaderror>





    <style>
      .cooldown_tips {
        margin: 30px auto;
        margin-top: 0;
        display: flex;
        align-items: center;
        padding: 10px;
        font-size: 14px;
        background-color: #f6f7f9;
        border-radius: 6px;
      }   
      .cooldown_tips_icon {
        display: block;
        width: 18px;
        height: 18px;
        margin-right: 8px;
      }
    </style>
  </head>

  <body id="activity-detail" class="zh_CN wx_wap_page 

                                            wx_wap_desktop_fontsize_2    mm_appmsg
 comment_feature
 discuss_tab appmsg_skin_default appmsg_style_default">
    
<script type="text/javascript" nonce="1682091926" reportloaderror>
  var biz = "" || "Mzg3NTczMDU2Mg==";
  var sn = "" || "41345986a28feb40bb7e80b985300b6f" || "";
  var mid = "" || "2247483828" || "";
  var idx = "" || "1" || "";
  window.__allowLoadResFromMp = true; // 允许从mp.weixin.qq.com加载js资源
  // window.__loadAllResFromMp = true; // 所有js资源都从mp域名加载
</script>

<script  nonce="1682091926" reportloaderror>
var page_begintime = (+new Date());
// 辟谣需求
var is_rumor = "";
var norumor = "";
if (!!(is_rumor * 1) && !(norumor*1) && !!biz && !!mid) {
  if (!document.referrer || document.referrer.indexOf("mp.weixin.qq.com/mp/rumor") == -1){
    location.href = "http://mp.weixin.qq.com/mp/rumor?action=info&__biz=" + biz + "&mid=" + mid + "&idx=" + idx + "&sn=" + sn + "#wechat_redirect";
  }
}
</script>


    <link rel="dns-prefetch" href="//res.wx.qq.com" reportloaderror>
<link rel="dns-prefetch" href="//mmbiz.qpic.cn" reportloaderror>
<link rel="dns-prefetch" href="https://wxa.wxs.qq.com" reportloaderror>
<link rel="shortcut icon" type="image/x-icon" href="//res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico" reportloaderror>
<link rel="mask-icon" href="//res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg" color="#4C4C4C" reportloaderror>
<link rel="apple-touch-icon-precomposed" href="//res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png" reportloaderror>
<script type="text/javascript" nonce="1682091926" reportloaderror>
String.prototype.html = function (encode) {
  var replace = ["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&yen;", "¥", "&amp;", "&"];
  // 最新版的safari 12有一个BUG，如果使用字面量定义一个数组，var a = [1, 2, 3]
  // 当调用了 a.reverse() 方法把变量 a 元素顺序反转成 3, 2, 1 后，
  // 即使此页面刷新了， 或者此页面使用 A标签、 window.open 打开的页面，
  // 只要调用到同一段代码， 变量 a 的元素顺序都会变成 3, 2, 1
  // 所以这里不用 reverse 方法
  /*
  if (encode) {
      replace.reverse();
  }*/
  var replaceReverse = ["&", "&amp;", "¥", "&yen;", "<", "&lt;", ">", "&gt;", " ", "&nbsp;", '"', "&quot;", "'", "&#39;"];
  var target;
  if (encode) {
    target = replaceReverse;
  } else {
    target = replace;
  }
  for (var i = 0, str = this; i < target.length; i += 2) {
    str = str.replace(new RegExp(target[i], 'g'), target[i + 1]);
  }
  return str;
};

window.isInWeixinApp = function () {
  return /MicroMessenger/.test(navigator.userAgent);
};

window.getQueryFromURL = function (url) {
  url = url || 'http://qq.com/s?a=b#rd'; // 做一层保护，保证URL是合法的
  var tmp = url.split('?'),
    query = (tmp[1] || "").split('#')[0].split('&'),
    params = {};
  for (var i = 0; i < query.length; i++) {
    var arg = query[i].split('=');
    params[arg[0]] = arg[1];
  }
  if (params['pass_ticket']) {
    params['pass_ticket'] = encodeURIComponent(params['pass_ticket'].html(false).html(false).replace(/\s/g, "+"));
  }
  return params;
};

(function () {
  var params = getQueryFromURL(location.href);
  window.uin = params['uin'] || "" || '';
  window.key = params['key'] || "" || '';
  window.wxtoken = params['wxtoken'] || '';
  window.pass_ticket = params['pass_ticket'] || '';
  window.appmsg_token = "";

  var ua = navigator.userAgent;
  if (ua.match(/Mac\sOS\sX\s(\d+[\.|_]\d+)/) || ua.match(/Windows(\s+\w+)?\s+?(\d+\.\d+)/) || ua.match(/Linux\s/)) {
    document.body.classList.add('pages_skin_pc');
  }
})();
</script>
    
<script type="text/javascript" nonce="1682091926" reportloaderror>window.PAGE_MID="mmbizwap:appmsg/newindex.html"</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>
  var write_sceen_time = (+new Date());
  var preview = "" * 1 || 0;
  var can_use_wecoin = '1' * 1; // 是否个人号
  var wecoin_tips = '0' * 1; // 是否出教育弹窗
  /* var can_use_wecoin = 1; */
  var wecoin_amount = '0' * 1; // 微信豆个数
  var preview_percent = '0' * 1;
</script>

<div id="js_article" style="position:relative;" class="rich_media">
  
  <div id="js_top_ad_area" class="top_banner"></div>
  
  <div id="js_base_container" class="rich_media_inner">
    
    
    <div id="page-content" class="rich_media_area_primary">
      <div class="rich_media_area_primary_inner">
        
        
        
                
        

        <div id="img-content" class="rich_media_wrp">
          
          <h1 class="rich_media_title " id="activity-name">
            
《源码探秘 CPython》19. 字符集和字符编码
          </h1>
          <div id="meta_content" class="rich_media_meta_list">
                                      <span id="copyright_logo" class="wx_tap_link js_wx_tap_highlight rich_media_meta icon_appmsg_tag appmsg_title_tag weui-wa-hotarea">原创</span>
                                                      <span class="rich_media_meta rich_media_meta_text">
                                      古明地觉
                                  </span>
                                      
                        <span class="rich_media_meta rich_media_meta_nickname" id="profileBt">
              <a href="javascript:void(0);" class="wx_tap_link js_wx_tap_highlight weui-wa-hotarea" id="js_name">
                古明地觉的编程教室              </a>
              <div id="js_profile_qrcode" aria-hidden="true" class="profile_container" style="display:none;">
                <div class="profile_inner">
                  <strong class="profile_nickname">古明地觉的编程教室</strong>
                  <img class="profile_avatar" id="js_profile_qrcode_img" src="" alt="">

                  <p class="profile_meta">
                  <label class="profile_meta_label">微信号</label>
                  <span class="profile_meta_value">unwind_exception</span>
                  </p>

                  <p class="profile_meta">
                  <label class="profile_meta_label">功能介绍</label>
                  <span class="profile_meta_value">Python、Rust 程序猿，你感兴趣的内容我都会写，点个关注吧(#^.^#)</span>
                  </p>
                </div>
                <span class="profile_arrow_wrp" id="js_profile_arrow_wrp">
                  <i class="profile_arrow arrow_out"></i>
                  <i class="profile_arrow arrow_in"></i>
                </span>
              </div>
            </span>
            <em id="publish_time" class="rich_media_meta rich_media_meta_text"></em>
            <em id="js_ip_wording_wrp" class="rich_media_meta rich_media_meta_text" role="option" style="display: none;">发表于<span id="js_ip_wording" ></span></em>

          </div>

          
                                                                              <div id="js_tags" class="article-tag__list single-tag__wrp js_single js_wx_tap_highlight wx_tap_card" data-len="1"
                        role="link" tabindex="0"
            aria-labelledby="js_article-tag-card__left js_a11y_comma js_article-tag-card__right"
                      >
                          
                                                <span aria-hidden="true" id="js_article-tag-card__left" class="article-tag-card__left">
                    <span class="article-tag-card__title">收录于合集</span>
                    <span class="article-tag__item-wrp no-active js_tag" data-url="https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&amp;action=getalbum&amp;album_id=2206970536067497985#wechat_redirect" data-tag_id="" data-album_id="2206970536067497985" data-tag_source="4">
                      <span class="article-tag__item">#CPython源码探秘</span>
                    </span>
                  </span>
                  <span aria-hidden="true" id="js_article-tag-card__right" class="article-tag-card__right">91个</span>
                                                    </div>

          
                    
                                        

          
                    

          
                              
                                        
                    
                    
          

          
          
                                                  <div class="rich_media_content js_underline_content              "
            id="js_content" style="visibility: hidden;"><p style="text-align: center;"><span style="color: rgb(217, 33, 66);"><strong><span style="color: rgb(217, 33, 66);font-size: 24px;">楔子</span></strong></span><br  /></p><p style="text-align: center;"><span style="color: rgb(217, 33, 66);"><strong><span style="color: rgb(217, 33, 66);font-size: 24px;"><br  /></span></strong></span></p><p>这一次我们分析一下Python的字符串，首先字符串是一个变长对象，因为不同长度的字符串所占的内存是不一样的；但同时字符串又是一个不可变对象，因为一旦创建就不可以再修改了。</p><p><br  /></p><p>而Python中的字符串是通过unicode来表示的，在底层对应的结构体是PyUnicodeObject。不过话说回来，为什么需要unicode呢?</p><p><br  /></p><p>首先计算机存储的基本单位是字节，由8个比特位组成，由于英文字母算上大小写只有52个，再加上若干字符，数量不会超过256个，因此一个字节完全可以表示。但是随着计算机的普及，越来越多的非英文字符出现，导致一个字节已经无法表示了。所以只能曲线救国，对于一个字节无法表示的字符，使用多个字节表示。</p><p><br  /></p><p><span style="color: rgb(172, 57, 255);">但是这样会出现两个问题：</span></p><ul class="list-paddingleft-2" style="list-style-type: disc;"><li><p>因为每个国家都有自己的字符编码，所以不支持多国语言，例如中文的编码不可以包含日文，否则就会造成乱码；</p></li><li><p>没有统一标准，例如中文有GB2312、GBK、GB18030等多个标准；</p></li></ul><p><br  /></p><p>到这里我们先不继续往下深入，我们先来理清楚一些概念。<br  /></p><p><br  /></p><p style="text-align: center;"><strong style="color: rgb(217, 33, 66);text-align: center;white-space: normal;"><span style="font-size: 24px;">字符集和字符编码</span></strong></p><p><strong style="color: rgb(217, 33, 66);text-align: center;white-space: normal;"><span style="font-size: 24px;"><br  /></span></strong></p><p>估计有很多小伙伴搞不清这两者的区别，我们先来解释一下所谓的字符集和字符编码是怎么一回事？</p><p><br  /></p><p><span style="color: rgb(172, 57, 255);"><strong>字符集</strong></span>：系统支持的所有字符组成的集合，像ASCII、GB2312、Big5、unicode都属于字符集。只不过不同的字符集所能容纳的字符个数不同，比如ASCII字符集中不包含中文，unicode则可以容纳世界上的所有字符；</p><p><br  /></p><p><strong style="color: rgb(172, 57, 255);white-space: normal;">字符编码</strong>：负责将每个字符转换成一个或多个计算机可以接受的具体数字，该数字可以理解为编号，因此字符编码维护了字符和编号之间的对应关系。而编码也分为多种，比如ascii、gbk、utf-8等等，字符编码不同，那么字符转换之后的编号也不同，当然能转化的字符种类也不同。比如ASCII这种字符编码，它就只能转换ASCII字符。</p><blockquote class="js_blockquote_wrap" data-type="2" data-url="" data-author-name="" data-content-utf8-length="57" data-source-title=""><section class="js_blockquote_digest"><p>当然，ASCII比较特殊，它既是字符集、也是字符编码。并且不管采用什么编码，ASCII字符对应的编号永远是相同的。</p></section></blockquote><p>将字符串中的每一个字符转成对应的编号，那么得到的就是<span style="color: rgb(0, 82, 255);"><strong>字节序列（bytes对象）</strong></span>，因为计算机存储和网络通讯的基本单位都是字节，所以字符串必须以字节序列的形式进行存储或传输。</p><p><br  /></p><p>因此字符串和字节序列在某种程度上是很相似的，字符串按照指定的编码进行encode即可得到字节序列，<span style="color: rgb(0, 82, 255);">也就是将每个字符都转成对应的编号</span>；字节序列按照相同的编码decode即可得到字符串，<span style="color: rgb(0, 82, 255);">也就是</span><span style="color: rgb(0, 82, 255);">根据编号找到对应的字符</span>。</p><p><br  /></p><p>比如我们写了一段文本，然后在存储的时候必须先进行编码，也就是将每一个字符都转成一个或多个系统可以接受的数字、即对应的编号之后，才可以进行存储。</p><section class="code-snippet__fix code-snippet__js"><ul class="code-snippet__line-index code-snippet__js"><li></li><li></li><li></li></ul><pre class="code-snippet__js" data-lang="makefile"><code><span class="code-snippet_outer">s = <span class="code-snippet__string">"你好"</span></span></code><code><span class="code-snippet_outer"><span class="code-snippet__comment">#&nbsp;编码之后就是一串数字</span></span></code><code><span class="code-snippet_outer">print(s.encode(<span class="code-snippet__string">"gbk"</span>))  <span class="code-snippet__comment"># b'\xc4\xe3\xba\xc3'</span></span></code></pre></section><p>假设文本中只有<span style="color: rgb(0, 82, 255);"><strong>你好</strong></span>二字，在存储的时候采用gbk进行编码，那么在读取的时候也必须使用gbk进行解码，否则的话就会无法解析而报错。因为字符编码不同，字符对应的编号也不同。<br  /></p><p><br  /></p><p>再比如每个国家都有自己的字符编码，你在日本的一台计算机上写好的文件拿到中国的计算机上打开，很有可能出现乱码。因为字符编码不同，字符和编号之间的对应关系也不同，采用不同的字符编码进行解析肯定会出问题。</p><p><br  /></p><p>但我们说，对于ASCII字符来说，由于不管采用哪一种编码，它们得到的编号都是固定的。所以编码对于ASCII字符来说，没有任何影响。</p><section class="code-snippet__fix code-snippet__js"><ul class="code-snippet__line-index code-snippet__js"><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li></ul><pre class="code-snippet__js" data-lang="python"><code><span class="code-snippet_outer">s = <span class="code-snippet__string">"abc"</span></span></code><code><span class="code-snippet_outer">print(s.encode(<span class="code-snippet__string">"gbk"</span>))  <span class="code-snippet__comment"># b'abc'</span></span></code><code><span class="code-snippet_outer">print(s.encode(<span class="code-snippet__string">"gbk"</span>).decode(<span class="code-snippet__string">"utf-8"</span>))  <span class="code-snippet__comment"># abc</span></span></code><code><span class="code-snippet_outer"><br  /></span></code><code><span class="code-snippet_outer"><span class="code-snippet__comment"># 但如果是非ASCII字符，就不行了</span></span></code><code><span class="code-snippet_outer"><span class="code-snippet__keyword">try</span>:</span></code><code><span class="code-snippet_outer">    s = <span class="code-snippet__string">"你好"</span></span></code><code><span class="code-snippet_outer">    s.encode(<span class="code-snippet__string">"gbk"</span>).decode(<span class="code-snippet__string">"utf-8"</span>)</span></code><code><span class="code-snippet_outer"><span class="code-snippet__keyword">except</span> UnicodeError <span class="code-snippet__keyword">as</span> e:</span></code><code><span class="code-snippet_outer">    <span class="code-snippet__comment"># 报错了，无法解析</span></span></code><code><span class="code-snippet_outer">    print(e)  </span></code><code><span class="code-snippet_outer">    <span class="code-snippet__comment"># 'utf-8' codec can't decode byte 0xc4 in position 0: invalid continuation byte</span></span></code><code><span class="code-snippet_outer"><br  /></span></code></pre></section><p>这里我们再回忆一下bytes对象，我们创建的时候可以采用字面量的方式，比如 <strong><span style="color: rgb(0, 82, 255);">b"abc"</span></strong>，但是 <span style="color: rgb(0, 82, 255);"><strong>b"憨"</strong></span>却不可以。原因就是<span style="color: rgb(0, 82, 255);"><strong>憨</strong></span>这个字符不是ASCII字符，那么采用不同的字符编码，其对应的编号是不同的，而这种方式Python又不知道我们使用哪一种编码，所以不允许这么做，而是需要通过<span style="color: rgb(0, 82, 255);"><strong>"憨".encode</strong></span>的方式手动指定<span style="color: rgb(0, 82, 255);"><strong>字符编码</strong></span>。</p><p><br  /></p><p>但是对于 ASCII 字符而言，不管采用哪一种字符编码，得到的编号都是一样的，&nbsp;所以Python针对ASCII字符则允许这种做法，比如<span style="color: rgb(0, 82, 255);"><strong>b"abc"</strong></span>。并且我们看到，对于汉字来说，在编码之后会对应多个编号，而每个编号占1字节，因此不同的字符所占的大小可能不同。</p><p><br  /></p><p><br  /></p><p style="text-align: center;"><strong style="text-align: center;white-space: normal;color: rgb(217, 33, 66);"><span style="font-size: 24px;">小结</span></strong></p><p><br  /></p><p>以上就是字符集和字符编码，字符集就是字符组成的集合，不同字符集所能容纳的字符数量是有限的。字符编码是将字符转成对应的编号，比如将一个字符串中的所有字符都转成对应的编号之后，就得到了字节序列。<br  /></p><p><br  /></p><p>当然和字符集一样，字符编码能转换的字符种类也是有限的，像汉字我们可以使用 gbk 编码、utf-8 编码，但是不能使用 ascii 编码。<br  /></p><p><br  /></p><p>以上算是理清楚了一些概念，显然过于简单了，主要是为后面的内容做铺垫。那么下一篇，就来从Python的角度分析字符串的存储方式。</p><p><br  /></p><p><br  /></p></div>

          <script type="text/javascript" nonce="1682091926" reportloaderror>
            var first_sceen__time = (+new Date());
            if ("" == 1 && document.getElementById('js_content')) {
              document.getElementById('js_content').addEventListener("selectstart",function(e){ e.preventDefault(); });
            }
          </script>
        </div>
                        <div id="js_tags_preview_toast" class="article-tag__error-tips" style="display: none;">预览时标签不可点</div>
                
        <div id="content_bottom_area" class="rich_media_tool_area"></div>

              </div>
    </div>

    <div class="rich_media_area_primary sougou" id="sg_tj" style="display:none"></div>

    
    <div class="rich_media_area_extra">
      <div class="rich_media_area_extra_inner">
        
        <div id="page_bottom_area"></div>
      </div>
    </div>

    
    <div id="js_pc_qr_code" class="qr_code_pc_outer" style="display:none;">
      <div class="qr_code_pc_inner">
        <div class="qr_code_pc">
          <img id="js_pc_qr_code_img" class="qr_code_pc_img">
          <p>微信扫一扫<br>关注该公众号</p>
        </div>
      </div>
    </div>
  </div>
</div>


<div class="wx_network_msg_wrp" id="js_network_msg_wrp"></div>


<script type="text/html" id="js_network_msg_load" nonce="1682091926" reportloaderror>
  <div class="wx_network_msg">
    <span role="img" aria-label="加载中" class="weui-primary-loading">
      <span class="weui-primary-loading__dot"></span>
    </span>
  </div>
</script>


<script type="text/html" id="js_network_msg_load_err" nonce="1682091926" reportloaderror>
  <div class="wx_network_msg">因网络连接问题，剩余内容暂无法加载。</div>
</script>


<div class="comment_primary_emotion_panel_wrp" id="js_emotion_panel_pc" style="display: none">
  <div class="comment_primary_emotion_panel">
    <ul class="comment_primary_emotion_list_pc" id="js_emotion_list_pc">
    </ul>
  </div>
</div>


<div class="weui-dialog__wrp" id="js_alert_panel" style="display:none;">
  <div class="weui-mask"></div>
  <div class="weui-dialog">
    <div class="weui-dialog__bd" id="js_alert_content"></div>
    <div class="weui-dialog__ft">
      <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_default" id="js_alert_confirm">知道了</a>
    </div>
  </div>
</div>


<script type="text/javascript" nonce="1682091926" reportloaderror>
  window.img_popup = 1; // 全量小程序弹窗
</script>


<div id="js_pc_weapp_code" class="weui-desktop-popover weui-desktop-popover_pos-up-center weui-desktop-popover_img-text weapp_code_popover" style="display: none;">
  <div class="weui-desktop-popover__inner">
      <div class="weui-desktop-popover__desc">
          <img id="js_pc_weapp_code_img">
          微信扫一扫<br>使用小程序<span id="js_pc_weapp_code_des"></span>
      </div>
  </div>
</div>
<div id="js_minipro_dialog" role="dialog" aria-modal="true" tabindex="0" aria-labelledby="js_minipro_dialog_head" style="display:none;">
  <div class="weui-mask"></div>
  <div class="weui-dialog weui-dialog_link">
      <div class="weui-dialog__hd">
          <strong class="weui-dialog__title" id="js_minipro_dialog_head" tabindex="0"></strong>
      </div>
      <div class="weui-dialog__bd" id="js_minipro_dialog_body"></div>
      
      <div class="weui-dialog__ft">
          <a role="button" id="js_minipro_dialog_cancel" href="javascript:void(0);" class="weui-dialog__btn weui-dialog__btn_default">取消</a>
          <a role="button" id="js_minipro_dialog_ok" href="javascript:void(0);" class="weui-dialog__btn weui-dialog__btn_primary">允许</a>
      </div>
  </div>
</div>
<div id="js_link_dialog" role="dialog" aria-modal="true" tabindex="0" aria-labelledby="js_link_dialog_body" style="display:none;">
  <div class="weui-mask"></div>
  <div class="weui-dialog weui-dialog_link">
    <div class="weui-dialog__hd">
      <strong class="weui-dialog__title" id="js_link_dialog_head" tabindex="0"></strong>
    </div>
    <div class="weui-dialog__bd" id="js_link_dialog_body" tabindex="0"></div>
    
    <div class="weui-dialog__ft">
      <a role="button" id="js_link_dialog_cancel" href="javascript:void(0);" class="weui-dialog__btn weui-dialog__btn_default">取消</a>
      <a role="button" id="js_link_dialog_ok" href="javascript:void(0);" class="weui-dialog__btn weui-dialog__btn_primary">允许</a>
    </div>
  </div>
</div>



    <script type="text/javascript" nonce="1682091926" reportloaderror>
window.logs.pagetime.page_begin = Date.now();

// // 广告iframe预加载
try {
  var adIframeUrl = localStorage.getItem('__WXLS_ad_iframe_url');
  if (window === top) {
    if (adIframeUrl) {
      if (navigator.userAgent.indexOf('iPhone') > -1) {
        var img = new Image();
        img.src = adIframeUrl;
      } else {
        var link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = adIframeUrl;
        document.getElementsByTagName('head')[0].appendChild(link);
      }
    }
  }
} catch (err) {

}
</script>
    

<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_colon">：</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_comma">，</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_period">。</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_space">&nbsp;</span>


<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_type_video">视频</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_type_weapp">小程序</span>


<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_zan_btn_txt">赞</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_zan_btn_tips">，轻点两下取消赞</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_like_btn_txt">在看</span>
<span aria-hidden="true" class="weui-a11y_ref" style="display:none" id="js_a11y_like_btn_tips">，轻点两下取消在看</span>

    <script type="text/javascript" nonce="1682091926" reportloaderror>
(function () {
  var totalCount = 0,
    finishCount = 0;

  function _addVConsole(uri, cb) {
    totalCount++;
    var node = document.createElement('SCRIPT');
    node.type = 'text/javascript';
    node.src = uri;
    node.setAttribute('nonce', '1682091926');
    if (cb) {
      node.onload = cb;
    }
    document.getElementsByTagName('head')[0].appendChild(node);
  }
  if (
    (document.cookie && document.cookie.indexOf('vconsole_open=1') > -1)
    || location.href.indexOf('vconsole=1') > -1
  ) {
    _addVConsole('https://mp.weixin.qq.com/mmbizappmsg/zh_CN/htmledition/js/scripts/vconsole-3.14.6.js', function () {
      var vConsole = new window.VConsole();
    });
  }

})();
</script>
    
    <script type="text/javascript" nonce="1682091926" reportloaderror>var __INLINE_SCRIPT__=function(){"use strict";var e=function(e,n){var t=e;if(e.indexOf("——")>-1){e=e.replace(/——/g,'<span style="letter-spacing:normal">——</span>')}n&&(n.innerHTML=n.innerHTML.replace(t,e))};if(!window.__second_open__){e("《源码探秘 CPython》19. 字符集和字符编码",document.getElementById("activity-name")),window.__setTitle=e}return e}();</script><script type="text/javascript" nonce="1682091926" reportloaderror>var __INLINE_SCRIPT__=function(){"use strict";var e=function(e,t,n,i){var _=new Date(1e3*(1*t)),o=function(e){return"0".concat(e).slice(-2)},r=_.getFullYear()+"-"+o(_.getMonth()+1)+"-"+o(_.getDate())+" "+o(_.getHours())+":"+o(_.getMinutes());i&&(i.innerText=r)};if(!window.__second_open__){e(0,"1643333400",0,document.getElementById("publish_time")),window.__setPubTime=e}return e}();</script>

<script type="text/javascript" nonce="1682091926" reportloaderror>
//兼容 IE
if (!window.console) window.console = { log: function() {} };
// 图片占位 @ekili
if (typeof getComputedStyle == 'undefined') {
  if (document.body.currentStyle) {
    window.getComputedStyle = function(el) {
      return el.currentStyle;
    }
  } else {
    window.getComputedStyle = {};
  }
}
// 图片和视频预加载逻辑，记得H5和秒开要对齐逻辑
(function(){
  window.__zoom = 1;

  var ua = navigator.userAgent.toLowerCase();
  var re = new RegExp("msie ([0-9]+[\.0-9]*)");
  var version;
  if (re.exec(ua) != null) {
    version = parseInt(RegExp.$1);
  }
  var isIE = false;
  if (typeof version != 'undefined' && version >= 6 && version <= 9) {
    isIE = true;
  }
  var isAccessibilityKey = 'isMpUserAccessibility';
  var isAccessMode = window.localStorage.getItem(isAccessibilityKey);
  var isCarton = isIE || '0' === '1' || '' === '1' || isAccessMode === '1';
  var bodyWidth = '' * 1;
  if (bodyWidth) {
    var styles = getComputedStyle(document.getElementById('page-content'));
    bodyWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingRight);
  }
  var getMaxWith = function () {
    var container = document.getElementById('img-content');
    var max_width = container.offsetWidth;
    !max_width && bodyWidth && (max_width = bodyWidth);
    var container_padding = 0;
    var container_style = getComputedStyle(container);
    container_padding = parseFloat(container_style.paddingLeft) + parseFloat(container_style.paddingRight);
    max_width -= container_padding;
    if (!max_width) {
      max_width = window.innerWidth - 30;      //防止offsetTop不可用，30为padding
    }
    return max_width;
  };
  var getParentWidth = function (dom) {
    var parent_width = 0;
    var parent = dom.parentNode;
    var outerWidth = 0;
    while (true) {
      if (!parent || parent.nodeType != 1) break;
      var parent_style = getComputedStyle(parent);
      if (!parent_style) break;
      parent_width = parent.clientWidth - parseFloat(parent_style.paddingLeft) - parseFloat(parent_style.paddingRight) - outerWidth;
      if (parent_width > 16) break; // 16是占位loading的宽度，所以要大于16
      outerWidth += parseFloat(parent_style.paddingLeft) + parseFloat(parent_style.paddingRight) + parseFloat(parent_style.marginLeft) + parseFloat(parent_style.marginRight) + parseFloat(parent_style.borderLeftWidth) + parseFloat(parent_style.borderRightWidth);
      parent = parent.parentNode;
    }
    return parent_width;
  }
  var getOuterW = function (dom) {
    var style = getComputedStyle(dom),
      w = 0;
    if (!!style) {
      w = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight) + parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth);
    }
    return w;
  };
  var getOuterH = function (dom) {
    var style = getComputedStyle(dom),
      h = 0;
    if (!!style) {
      h = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom) + parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
    }
    return h;
  };
  var insertAfter = function (dom, afterDom) {
    var _p = afterDom.parentNode;
    if (!_p) {
      return;
    }
    if (_p.lastChild === afterDom) {
      _p.appendChild(dom);
    } else {
      _p.insertBefore(dom, afterDom.nextSibling);
    }
  };
  var getQuery = function (name, url) {
    //参数：变量名，url为空则表从当前页面的url中取
    var u = arguments[1] || window.location.search,
      reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"),
      r = u.substr(u.indexOf("\?") + 1).match(reg);
    return r != null ? r[2] : "";
  };

  /**
    * 设置图片size
    *
    * @param {HTMLElement} item             图片元素
    * @param {number} widthNum         宽度数值
    * @param {string} widthUnit        宽度单位
    * @param {number} ratio            宽高比
    * @param {boolean} breakParentWidth 是否突破父元素宽度(父元素是否被撑大)
    */
  function setImgSize(item, widthNum, widthUnit, ratio, breakParentWidth) {
    setTimeout(function () {
      var img_padding_border = getOuterW(item) || 0;
      var img_padding_border_top_bottom = getOuterH(item) || 0;

      // 如果设置的宽度超过了父元素最大宽度，则取父元素宽度
      if (widthNum > getParentWidth(item) && !breakParentWidth) {
        widthNum = getParentWidth(item);
      }

      var height = (widthNum - img_padding_border) * ratio + img_padding_border_top_bottom;

      if (isCarton) { // 判一下是不是漫画原创，如果是，不走懒加载
        var url = item.getAttribute('data-src');
        item.src = url;

        // 不走懒加载但是需要跟懒加载一样去除占位高度
        item.style.height = 'auto';
      } else {
        // if (parseFloat(widthNum, 10) > 40 && height > 40 && breakParentWidth) {
        //   item.className += ' img_loading';
        // }
        // item.src = "data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==";
        widthNum !== 'auto' && (item.style.cssText += ";width: " + widthNum + widthUnit + " !important;");
        widthNum !== 'auto' && (item.style.cssText += ";height: " + height + widthUnit + " !important;");
      }
    }, 10);
  }
  // 图片和视频预加载逻辑，记得H5和秒开要对齐逻辑
  // (function () {
  //   var images = document.getElementsByTagName('img');
  //   var length = images.length;
  //   var max_width = getMaxWith();
  //   for (var i = 0; i < length; ++i) {
  //     if (window.__second_open__ && images[i].getAttribute('__sec_open_place_holder__')) {
  //       continue;
  //     }
  //     var imageItem = images[i];
  //     // var imgPlaceHolder = document.createElement('img');
  //     var src_ = imageItem.getAttribute('data-src');
  //     var realSrc = imageItem.getAttribute('src');
  //     if (!src_ || realSrc) continue;
  //     // 图片原始宽度
  //     var originWidth = imageItem.getAttribute('data-w');
  //     var ratio_ = 1 * imageItem.getAttribute('data-ratio');
  //     var imgStyle = imageItem.getAttribute('style');
  //     imageItem.setAttribute('data-index', i);

  //     var height = 100;
  //     if (ratio_ && ratio_ > 0) {
  //       // 非漫画才需要占位
  //       if (!isCarton) {
  //         const imgWrap = document.createElement('span');

  //         // imgWrap.className = "js_img_placeholder wx_widget_placeholder_wrp";
  //         // imgWrap.style = imgStyle;
  //         // imgWrap.setAttribute("data-index", i);
  //         // 用自己当占位的好处：不用担心新的img跟渲染出来的位置宽高不一致
  //         // imageItem.setAttribute('data-origin-display', imageItem.style.display);
  //         // imageItem.style.display = 'none';
  //         imageItem.classList.add("js_img_placeholder", "wx_img_placeholder");
  //         // imageItem.className = "js_img_placeholder wx_img_placeholder";
  //         imageItem.src = "data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E";

  //         // imgPlaceHolder.className = "js_img_placeholder wx_img_placeholder";
  //         // imgPlaceHolder.setAttribute("data-src", src_ || realSrc);
  //         // imgPlaceHolder.setAttribute("data-index", i);
  //         // imgPlaceHolder.style = imgStyle;
  //         // imgPlaceHolder.src = "data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E";
  //         // imgWrap.append(imgPlaceHolder);

  //         // insertAfter(imgPlaceHolder, imageItem);
  //       }

  //       var parent_width = getParentWidth(imageItem) || max_width;
  //       var initWidth = imageItem.style.width || imageItem.getAttribute('width') || originWidth || parent_width;
  //       if(initWidth === 'inherit') {
  //         initWidth = parent_width;
  //       }
  //       initWidth = parseFloat(initWidth, 10) > max_width ? max_width : initWidth;
  //       // 有attribute或style中的width，写入_width属性，在图片加载完成时写入img标签
  //       if (initWidth) {
  //         imageItem.setAttribute('_width', !isNaN(initWidth * 1) ? initWidth + 'px' : initWidth);
  //       }
  //       // 使用百分比，则计算出像素宽度
  //       if (typeof initWidth === 'string' && initWidth.indexOf('%') !== -1) {
  //         initWidth = parseFloat(initWidth.replace('%', ''), 10) / 100 * parent_width;
  //       }
  //       // 使用auto，就是原始宽度
  //       if (initWidth === 'auto') {
  //         initWidth = originWidth;
  //         if (originWidth === 'auto') {
  //           initWidth = parent_width;
  //         } else {
  //           initWidth = originWidth;
  //         }
  //       }

  //       var widthNum;
  //       var widthUnit;
  //       if (initWidth === 'auto') {
  //         widthNum = 'auto';
  //       } else {
  //         var res = /^(\d+(?:\.\d+)?)([a-zA-Z%]+)?$/.exec(initWidth);
  //         widthNum = res && res.length >= 2 ? res[1] : 0;
  //         widthUnit = res && res.length >= 3 && res[2] ? res[2] : 'px';
  //       }

  //       // 试探一下parent宽度在设置了图片的大小之后是否会变化
  //       // if (!isCarton) {
  //       //   setImgSize(imgPlaceHolder, widthNum, widthUnit, ratio_, true);
  //       // } else {
  //       //   setImgSize(imageItem, widthNum, widthUnit, ratio_, true);
  //       // }

  //       setImgSize(imageItem, widthNum, widthUnit, ratio_, true);

  //       // // 真正设置宽高
  //       // (function (item, widthNumber, unit, ratio) {
  //       //   setTimeout(function () {
  //       //     setImgSize(item, widthNumber, unit, ratio, false);
  //       //   });
  //       // })(imageItem, widthNum, widthUnit, ratio_);
  //     } else {
  //       // 这里使用visibility 而不是display none 是因为没有占位元素，那就让图片自己占位
  //       imageItem.style.cssText += ";visibility: hidden !important;";
  //     }
  //   }
  // })();
  window.__videoDefaultRatio = 16 / 9;//默认值是16/9
  window.__getVideoWh = function (dom) {
    var max_width = getMaxWith(),
      width = max_width,
      ratio_ = dom.getAttribute('data-ratio') * 1,//mark16/9
      arr = [4 / 3, 16 / 9],
      ret = arr[0],
      abs = Math.abs(ret - ratio_);
    if (!ratio_) { // 没有比例
      if (dom.getAttribute("data-mpvid")) { // MP视频
        ratio_ = 16 / 9;
      } else { // 非MP视频，需要兼容历史图文
        ratio_ = 4 / 3;
      }
    } else { // 有比例，则判断更接近4/3还是更接近16/9
      for (var j = 1, jl = arr.length; j < jl; j++) {
        var _abs = Math.abs(arr[j] - ratio_);
        if (_abs < abs) {
          abs = _abs;
          ret = arr[j];
        }
      }
      ratio_ = ret;
    }

    var parent_width = getParentWidth(dom) || max_width,
      width = width > parent_width ? parent_width : width,
      outerW = getOuterW(dom) || 0,
      outerH = getOuterH(dom) || 0,
      videoW = width - outerW,
      videoH = videoW / ratio_,
      speedDotH = 12, // 播放器新样式的进度条在最下面，为了避免遮住拖动的点点，需要额外设置高一些
      height = videoH + outerH + speedDotH;

    return { w: Math.ceil(width), h: Math.ceil(height), vh: videoH, vw: videoW, ratio: ratio_, sdh: speedDotH };
  };

  // 图片和视频预加载逻辑，记得H5和秒开要对齐逻辑
  (function () {
    var iframe = document.getElementsByTagName('iframe');
    for (var i = 0, il = iframe.length; i < il; i++) {
      if (window.__second_open__ && iframe[i].getAttribute('__sec_open_place_holder__')) {
        continue;
      }
      var a = iframe[i];
      var src_ = a.getAttribute('src') || a.getAttribute('data-src') || "";

      /* if (!/^http(s)*\:\/\/v\.qq\.com\/iframe\/(preview|player)\.html\?/.test(src_)
        && !/^http(s)*\:\/\/mp\.weixin\.qq\.com\/mp\/readtemplate\?t=pages\/video_player_tmpl/.test(src_)
      ) {
        continue;
      } */
      var vid = getQuery("vid", src_) || a.getAttribute('data-mpvid');
      if (!vid) {
        continue;
      }
      vid = vid.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "");//清除前后空格
      a.removeAttribute('src');
      a.style.display = "none";
      var obj = window.__getVideoWh(a),
        videoPlaceHolderSpan = document.createElement('span');

      videoPlaceHolderSpan.className = "js_img_placeholder wx_widget_placeholder";
      videoPlaceHolderSpan.setAttribute("data-vid", vid);
      videoPlaceHolderSpan.innerHTML = '<span class="weui-primary-loading"><span class="weui-primary-loading__dot"></span></span>';
      videoPlaceHolderSpan.style.cssText = "width: " + obj.w + "px !important;";

      insertAfter(videoPlaceHolderSpan, a); // 在视频后面插入占位

      /* var parentNode = a.parentNode;
      var copyIframe = a;
      var index = i; */

      // 由于视频需要加一个转载的来源，所以这里需要提前设置高度
      function ajax(obj) {
        var url = obj.url;
        var xhr = new XMLHttpRequest();

        var data = null;
        if (typeof obj.data == "object") {
          var d = obj.data;
          data = [];
          for (var k in d) {
            if (d.hasOwnProperty(k)) {
              data.push(k + "=" + encodeURIComponent(d[k]));
            }
          }
          data = data.join("&");
        } else {
          data = typeof obj.data == 'string' ? obj.data : null;
        }

        xhr.open('POST', url, true);
        xhr.onreadystatechange = function () {
          if (xhr.readyState == 4) {
            if (xhr.status >= 200 && xhr.status < 400) {
              obj.success && obj.success(xhr.responseText);
            } else {
              obj.error && obj.error(xhr);
            }
            obj.complete && obj.complete();
            obj.complete = null;
          }
        };
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.send(data);
      }

      var mid = "2247483828" || "" || "";
      var biz = "Mzg3NTczMDU2Mg==" || "";
      var sessionid = "" || "svr_205d18c9313";
      var idx = "1" || "";

      (function sendReq(parentNode, copyIframe, index, vid) {
        ajax({
          url: '/mp/videoplayer?vid=' + vid + '&mid=' + mid + '&idx=' + idx + '&__biz=' + biz + '&sessionid=' + sessionid + '&f=json',
          type: "GET",
          dataType: 'json',
          success: function (json) {
            var ret = JSON.parse(json || '{}');
            var ori = ret.ori_status;
            var hit_biz_headimg = ret.hit_biz_headimg + '/64';
            var hit_nickname = ret.hit_nickname;
            var hit_username = ret.hit_username;
            var sourceBiz = ret.source_encode_biz;

            var selfUserName = "gh_24891280c13f";

            if (ori === 2 && selfUserName !== hit_username) {
              var videoBar = document.createElement('div');
              var videoBarHtml = '<div class="wx-edui-video_source_link js_wx_tap_highlight wx_tap_card" id="' + (hit_username + index) + '" data-hit-username="' + hit_username + '" data-hit-biz="' + sourceBiz + '">';
              videoBarHtml += '<div class="wx-edui-video_source_word">以下视频来源于</div>';
              videoBarHtml += '<div class="wx-edui-video_account_info">';
              videoBarHtml += '<div class="wx-edui-video_account_avatar" id="' + (hit_biz_headimg + index) + '" data-src="' + hit_biz_headimg + '"></div>';
              videoBarHtml += '<div class="wx-edui-video_account_name">' + hit_nickname + '</div>';
              videoBarHtml += '<i class="wx-edui-video_account_arrow"></i>';
              videoBarHtml += '</div>';
              videoBarHtml += '<div class="wx-edui-video_source_link__layer_mask"></div>';
              videoBarHtml += '</div>';
              videoBar.innerHTML = videoBarHtml;
              var spanContainer = document.getElementById('js_mp_video_container_' + index);
              if (spanContainer) {
                spanContainer.parentNode.insertBefore(videoBar, spanContainer);
              } else if (parentNode.contains && parentNode.contains(copyIframe)) {
                parentNode.insertBefore(videoBar, copyIframe);
              } else {
                parentNode.insertBefore(videoBar, parentNode.firstElementChild);
              }
              var avatorEle = document.getElementById(hit_biz_headimg + index);
              var avatorSrc = avatorEle.dataset.src;
              console.log('avatorSrc' + avatorSrc);
              if (ret.hit_biz_headimg) {
                avatorEle.style.backgroundImage = 'url(' + avatorSrc + ')';
              }
            }
          },
          error: function (xhr) {
          }
        });
      })(a.parentNode, a, i, vid);

      a.style.cssText += ";width: " + obj.w + "px !important;";
      a.setAttribute("width", obj.w);
      if (window.__zoom != 1) {
        a.style.display = "block";
        videoPlaceHolderSpan.style.display = "none";
        a.setAttribute("_ratio", obj.ratio);
        a.setAttribute("_vid", vid);
      } else {
        videoPlaceHolderSpan.style.cssText += "height: " + (obj.h - obj.sdh) + "px !important;margin-bottom: " + obj.sdh + "px !important;";
        a.style.cssText += "height: " + obj.h + "px !important;";
        a.setAttribute("height", obj.h);
      }
      a.setAttribute("data-vh", obj.vh);
      a.setAttribute("data-vw", obj.vw);
      if (a.getAttribute("data-mpvid")) {
        a.setAttribute("data-src", location.protocol + "//mp.weixin.qq.com/mp/readtemplate?t=pages/video_player_tmpl&auto=0&vid=" + vid);
      } else {
        a.setAttribute("data-src", location.protocol + "//v.qq.com/iframe/player.html?vid=" + vid + "&width=" + obj.vw + "&height=" + obj.vh + "&auto=0");
      }
    }
  })();

  (function () {
    if (window.__zoom != 1) {
      if (!window.__second_open__) {
        document.getElementById('page-content').style.zoom = window.__zoom;
        var a = document.getElementById('activity-name');
        var b = document.getElementById('meta_content');
        if (!!a) {
          a.style.zoom = 1 / window.__zoom;
        }
        if (!!b) {
          b.style.zoom = 1 / window.__zoom;
        }
      }
      var images = document.getElementsByTagName('img');
      for (var i = 0, il = images.length; i < il; i++) {
        if (window.__second_open__ && images[i].getAttribute('__sec_open_place_holder__')) {
          continue;
        }
        images[i].style.zoom = 1 / window.__zoom;
      }
      var iframe = document.getElementsByTagName('iframe');
      for (var i = 0, il = iframe.length; i < il; i++) {
        if (window.__second_open__ && iframe[i].getAttribute('__sec_open_place_holder__')) {
          continue;
        }
        var a = iframe[i];
        a.style.zoom = 1 / window.__zoom;
        var src_ = a.getAttribute('data-src') || "";
        if (!/^http(s)*\:\/\/v\.qq\.com\/iframe\/(preview|player)\.html\?/.test(src_)
          && !/^http(s)*\:\/\/mp\.weixin\.qq\.com\/mp\/readtemplate\?t=pages\/video_player_tmpl/.test(src_)
        ) {
          continue;
        }
        var ratio = a.getAttribute("_ratio");
        var vid = a.getAttribute("_vid");
        a.removeAttribute("_ratio");
        a.removeAttribute("_vid");
        var vw = a.offsetWidth - (getOuterW(a) || 0);
        var vh = vw / ratio;
        var h = vh + (getOuterH(a) || 0)
        a.style.cssText += "height: " + h + "px !important;"
        a.setAttribute("height", h);
        if (/^http(s)*\:\/\/v\.qq\.com\/iframe\/(preview|player)\.html\?/.test(src_)) {
          a.setAttribute("data-src", location.protocol + "//v.qq.com/iframe/player.html?vid=" + vid + "&width=" + vw + "&height=" + vh + "&auto=0");
        }
        a.style.display = "none";
        var parent = a.parentNode;
        if (!parent) {
          continue;
        }
        for (var j = 0, jl = parent.children.length; j < jl; j++) {
          var child = parent.children[j];
          if (child.className.indexOf("js_img_placeholder") >= 0 && child.getAttribute("data-vid") == vid) {
            child.style.cssText += "height: " + h + "px !important;";
            child.style.display = "";
          }
        }
      }
    }
  })();
})();
</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>!function(){"use strict";function t(e){return t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},t(e)}window.__page_cls_ctrl__canRenderSilently=!("__page_cls_ctrl__canRenderSilently"in window)||window.__page_cls_ctrl__canRenderSilently,window.__page_cls_ctrl__forceRenderSilentlyList="__page_cls_ctrl__forceRenderSilentlyList"in window?window.__page_cls_ctrl__forceRenderSilentlyList:[],window.__page_cls_ctrl__compRenderInfo="__page_cls_ctrl__compRenderInfo"in window?window.__page_cls_ctrl__compRenderInfo:{};var e={defaultContentTpl:'<span class="js_img_placeholder wx_widget_placeholder" style="width:#width#px !important;height:#height#px !important;text-indent: 0"><span class="weui-primary-loading"><span class="weui-primary-loading__dot"></span></span>',config:[{querySelector:"redpacketcover",genId:function(){return decodeURIComponent((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-coveruri")||"")},calW:function(){return.7854*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return this.calW({parentWidth:t.parentWidth})/.73346+27+37},replaceContentCssText:"",outerContainerRight:"</section>"},{querySelector:"qqmusic",genId:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return(t.node.getAttribute("musicid")||"").replace(/^\s/,"").replace(/\s$/,"")+"_"+t.index},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 88},replaceContentCssText:"",appendContentCssText:"margin-top:16px;diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpvoice",genId:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return decodeURIComponent(t.node.getAttribute("voice_encode_fileid")||"").replace(/^\s/,"").replace(/\s$/,"")+"_"+t.index},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return t.node.getAttribute("data-topic_id")&&t.node.getAttribute("data-topic_name")?167:122},replaceContentCssText:"",appendContentCssText:"margin-top:16px;diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mppoi",genId:function(){return(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-id")||""},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 219},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpsearch",genId:function(){return decodeURIComponent("mp-common-search")},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 100},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpvideosnap",genId:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return"live"===(t.node.getAttribute("data-type")||"video")?decodeURIComponent(t.node.getAttribute("data-noticeid")||""):decodeURIComponent(t.node.getAttribute("data-id")||"")},calW:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.node.getAttribute("data-type")||"video",n=t.node.getAttribute("data-width")||"",i=t.node.getAttribute("data-height")||"";if("live"===e||"topic"===e)return t.parentWidth;var r,o=1,a=0,d=!1;return 1===(o=n/i)||o===3/4||(o===4/3||o===16/9?d=!0:o<3/4?o=3/4:o>1&&o<4/3?o=1:o>4/3?d=!0:("number"!=typeof o||Object.is(o,NaN))&&(o=1)),t.node.setAttribute("data-ratio",o),t.node.setAttribute("data-isHorizontal",d),r=(a=!0===d?t.parentWidth:window.innerWidth<1024?.65*window.innerWidth:.65*t.parentWidth)/o,t.node.setAttribute("data-computedWidth",a),t.node.setAttribute("data-computedHeight",r),a},calH:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.node.getAttribute("data-desc")||"",n=t.node.getAttribute("data-type")||"video",i=t.node.getAttribute("data-computedHeight")||"";switch(n){case"live":return e?152:116;case"topic":return 201;case"image":case"video":return parseFloat(i)}},getBorderRadius:function(){return"video"===((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-type")||"video")?4:8},replaceContentCssText:"",appendContentCssText:"display:flex;margin:16px auto;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mp-wxaproduct",genId:function(){return decodeURIComponent((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-wxaproduct-productid")||"")},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return"mini"===((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-wxaproduct-cardtype")||"")?124:466},replaceContentCssText:"",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpprofile",genId:function(t){return t.node.getAttribute("data-id")||""},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 143},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mp-common-sticker",genId:function(t){return t.node.getAttribute("data-md5")||""},calW:function(){return 120},calH:function(){return 120},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:'<div style="display: flex; justify-content: center;">',outerContainerRight:"</div>"}]};function n(){!function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};if("function"==typeof document.querySelectorAll)for(var e={maxWith:document.getElementById("img-content").getBoundingClientRect().width,idAttr:"data-preloadingid"},n=0,i=t.config.length;n<i;n++)for(var r=t.config[n],o=document.querySelectorAll(r.querySelector),a=0,d=o.length;a<d;a++){var c=o[a],s=c.parentNode.getBoundingClientRect().width;if(s=Math.min(s,e.maxWith),!c.getAttribute("has-insert-preloading")){var l=r.calW({parentWidth:s,node:c}),u=r.calH({parentWidth:s,node:c}),p=r.genId({index:a,node:c}),g="function"==typeof r.getBorderRadius?r.getBorderRadius({index:a,node:c}):8,h=t.defaultContentTpl.replace(/#height#/g,u).replace(/#width#/g,l).replace(/#borderRadius#/g,g),_=document.createElement("div");if(_.innerHTML=h,r.replaceContentCssText){var f=r.replaceContentCssText.replace(/#height#/g,u).replace(/#width#/g,l);_.firstChild.style.cssText=f}else r.appendContentCssText&&(_.firstChild.style.cssText+=r.appendContentCssText);var m=r.outerContainerLeft+_.innerHTML+r.outerContainerRight;_.innerHTML=m,_.firstChild.setAttribute(e.idAttr,p),c.parentNode.insertBefore(_.firstChild,c.nextSibling),c.setAttribute("has-insert-preloading","1")}}}(e)}function i(t){for(var e=((t=t||"http://qq.com/s?a=b#rd").split("?")[1]||"").split("#")[0].split("&"),n={},i=0;i<e.length;i++){var r=e[i].indexOf("=");if(r>-1)n[e[i].substring(0,r)]=e[i].substring(r+1)}return n.pass_ticket&&(n.pass_ticket=encodeURIComponent(function(t){for(var e=["&#96;","`","&#39;","'","&quot;",'"',"&nbsp;"," ","&gt;",">","&lt;","<","&yen;","¥","&amp;","&"],n=0;n<e.length;n+=2)t=t.replace(new RegExp(e[n],"g"),e[n+1]);return t}(n.pass_ticket).replace(/\s/g,"+"))),n}function r(){var t=document.getElementById("img-content"),e=t.offsetWidth,n=getComputedStyle(t);return(e-=parseFloat(n.paddingLeft)+parseFloat(n.paddingRight))||(e=window.innerWidth-32),e}function o(t){for(var e=0,n=t.parentNode,i=0;n&&1===n.nodeType;){var r=getComputedStyle(n);if(!r)break;if((e=n.clientWidth-parseFloat(r.paddingLeft)-parseFloat(r.paddingRight)-i)>16)break;i+=parseFloat(r.paddingLeft)+parseFloat(r.paddingRight)+parseFloat(r.marginLeft)+parseFloat(r.marginRight)+parseFloat(r.borderLeftWidth)+parseFloat(r.borderRightWidth),n=n.parentNode}return e<0?0:e}function a(t){var e=getComputedStyle(t),n=0;return e&&(n=parseFloat(e.paddingLeft)+parseFloat(e.paddingRight)+parseFloat(e.borderLeftWidth)+parseFloat(e.borderRightWidth)),n}function d(t){var e=getComputedStyle(t),n=0;return e&&(n=parseFloat(e.paddingTop)+parseFloat(e.paddingBottom)+parseFloat(e.borderTopWidth)+parseFloat(e.borderBottomWidth)),n}function c(t,e,n,i,r){var c=a(t)||0,s=d(t)||0;e>o(t)&&!r&&(e=o(t));var l=(e-c)*i+s;"auto"!==e&&(t.style.cssText+=";width: ".concat(e).concat(n," !important;")),"auto"!==e&&(t.style.cssText+=";height: ".concat(l).concat(n," !important;"))}"undefined"==typeof getComputedStyle&&(document.body.currentStyle?window.getComputedStyle=function(t){return t.currentStyle}:window.getComputedStyle={});var s="js_img_placeholder",l=window.localStorage.getItem("isMpUserAccessibility"),u=","+[.875,1,1.125,1.25,1.375].join(",")+",",p=window.location.href.match(/winzoom=(\d+(?:\.\d+)?)/);if(p&&p[1]){var g=parseFloat(p[1]);u.indexOf(","+g+",")}var h=navigator.userAgent;/mac\sos/i.test(h)&&!/(iPhone|iPad|iPod|iOS)/i.test(h)||/windows\snt/i.test(h);!function(e,u,p){if(document.body.clientWidth&&document.getElementById("img-content")&&document.getElementById("img-content").offsetWidth){for(var g=function(e,n){if(window.__second_open__&&u[e].getAttribute("__sec_open_place_holder__"))return"continue";var c=u[e],l=i(c.getAttribute("src")||c.getAttribute("data-src")||"").vid||c.getAttribute("data-mpvid");if(!l)return"continue";l=l.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,""),c.removeAttribute("src"),c.style.display="none";var g,h,_,f=function(t){for(var e=r(),n=e,i=1*t.getAttribute("data-ratio")||4/3,c=[4/3,16/9],s=c[0],l=Math.abs(s-i),u=1,p=c.length;u<p;u++){var g=Math.abs(c[u]-i);g<l&&(l=g,s=c[u])}i=s;var h=o(t)||e,_=n>h?h:n,f=_-(a(t)||0),m=f/i,v=m+(d(t)||0)+12;return{w:Math.ceil(_),h:Math.ceil(v),vh:m,vw:f,ratio:i,sdh:12}}(c),m=document.createElement("span");m.className="".concat(s," wx_widget_placeholder"),m.setAttribute("data-vid",l),m.innerHTML='<span class="weui-primary-loading"><span class="weui-primary-loading__dot"></span></span>',m.style.cssText="width: "+f.w+"px !important;",g=m,(_=(h=c).parentNode)&&(_.lastChild===h?_.appendChild(g):_.insertBefore(g,h.nextSibling)),c.style.cssText+=";width: "+f.w+"px !important;",c.setAttribute("width",f.w),m.style.cssText+="height: "+(f.h-f.sdh)+"px !important;margin-bottom: "+f.sdh+"px !important;",c.style.cssText+="height: "+f.h+"px !important;",c.setAttribute("height",f.h),c.setAttribute("data-vh",f.vh),c.setAttribute("data-vw",f.vw),c.setAttribute("data-src","https://v.qq.com/iframe/player.html?vid="+l+"&width="+f.vw+"&height="+f.vh+"&auto=0"),c.setAttribute("__sec_open_place_holder__",!0);var v=c.parentNode,y=c,w=e,C=window.dataaaa.mid,b=window.dataaaa.bizuin,x=window.dataaaa.idx;!function(e){var n=e.url,i=new XMLHttpRequest,r=null;if("object"===t(e.data)){var o=e.data;for(var a in r=[],o)o.hasOwnProperty(a)&&r.push(a+"="+encodeURIComponent(o[a]));r=r.join("&")}else r="string"==typeof e.data?e.data:null;i.open("POST",n,!0),i.onreadystatechange=function(){4===i.readyState&&(i.status>=200&&i.status<400?e.success&&e.success(i.responseText):e.error&&e.error(i),e.complete&&e.complete(),e.complete=null)},i.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=UTF-8"),i.setRequestHeader("X-Requested-With","XMLHttpRequest"),i.send(r)}({url:"mp/videoplayer?vid=".concat(l,"&mid=").concat(C,"&idx=").concat(x,"&__biz=").concat(b,"&f=json"),type:"GET",dataType:"json",success:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"{}",e=JSON.parse(t),n=e.ori_status,i=e.hit_biz_headimg+"/64",r=e.hit_nickname,o=e.hit_username;if(2===n&&o!==p.user_name){var a=document.createElement("div");a.innerHTML='<div class="wx-edui-video_source_link" id="'.concat(o+w,'" data-hit-username="').concat(o,'">')+'<div class="video_source_word">以下视频来源于</div><div class="wx-edui-video_account_info">'+'<div class="wx-edui-video_account_avatar" id="'.concat(i+w,'" data-src="').concat(i,'"></div>')+'<div class="wx-edui-video_account_name">'.concat(r,"</div>")+'<i class="wx-edui-video_account_arrow"></i></div></div><div class="wx-edui-video_source_link__layer_mask"></div>';var d=document.getElementById("js_mp_video_container_"+w);d?d.parentNode.insertBefore(a,d):v.contains&&v.contains(y)?v.insertBefore(a,y):v.insertBefore(a,v.firstElementChild);var c=document.getElementById(i+w),s=c.dataset.src;console.log("avatorSrc"+s),e.hit_biz_headimg&&(c.style.backgroundImage="url(".concat(s,")"))}},error:function(t){}})},h=0,_=u.length;h<_;h++)g(h);for(var f=1*p.copyright_info.is_cartoon_copyright||1*p.user_info.is_care_mode||"1"===l,m=r(),v=0,y=e.length;v<y;v++)if(!window.__second_open__||!e[v].getAttribute("__sec_open_place_holder__")){var w=e[v],C=w.getAttribute("data-src"),b=w.getAttribute("src");if(C&&!b){w.getAttribute("style");var x=w.dataset.w,A=1*w.dataset.ratio;w.setAttribute("data-index",v);var T=0,R="px";if(A&&A>0){f||(w.classList.add(s,"wx_img_placeholder"),w.src="data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E");var W=o(w)||m,S=w.style.width||w.getAttribute("width")||x||W;"inherit"===(S=parseFloat(S,10)>m?m:S)&&(S=W),S&&w.setAttribute("_width",isNaN(1*S)?S:S+"px"),"string"==typeof S&&-1!==S.indexOf("%")&&(S=parseFloat(S.replace("%",""),10)/100*W)<Number(x)&&(S=x),"auto"===S&&(S=x,S="auto"!==x&&x?x:W);var F=/^(\d+(?:\.\d+)?)([a-zA-Z%]+)?$/.exec(S);T=F&&F.length>=2?F[1]:0,R=F&&F.length>=3&&F[2]?F[2]:"px";var I=T;f?(w.src=C,w.style.height="auto"):(c(w,I,R,A,!0),c(w,I,R,A,!1))}else w.style.cssText+=";visibility: hidden !important;";p.is_h5_render||w.setAttribute("__sec_open_place_holder__",!0)}}n()}}(document.getElementsByTagName("img"),[],{is_h5_render:!0,user_name:"gh_24891280c13f",copyright_info:{is_cartoon_copyright:"0"},user_info:{is_care_mode:""}})}();</script><script type="text/javascript" nonce="1682091926" reportloaderror>!function(){"use strict";window.__page_cls_ctrl__canRenderSilently=!("__page_cls_ctrl__canRenderSilently"in window)||window.__page_cls_ctrl__canRenderSilently,window.__page_cls_ctrl__forceRenderSilentlyList="__page_cls_ctrl__forceRenderSilentlyList"in window?window.__page_cls_ctrl__forceRenderSilentlyList:[],window.__page_cls_ctrl__compRenderInfo="__page_cls_ctrl__compRenderInfo"in window?window.__page_cls_ctrl__compRenderInfo:{};var e={defaultContentTpl:'<span class="js_img_placeholder wx_widget_placeholder" style="width:#width#px !important;height:#height#px !important;text-indent: 0"><span class="weui-primary-loading"><span class="weui-primary-loading__dot"></span></span>',config:[{querySelector:"redpacketcover",genId:function(){return decodeURIComponent((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-coveruri")||"")},calW:function(){return.7854*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return this.calW({parentWidth:e.parentWidth})/.73346+27+37},replaceContentCssText:"",outerContainerRight:"</section>"},{querySelector:"qqmusic",genId:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return(e.node.getAttribute("musicid")||"").replace(/^\s/,"").replace(/\s$/,"")+"_"+e.index},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 88},replaceContentCssText:"",appendContentCssText:"margin-top:16px;diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpvoice",genId:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return decodeURIComponent(e.node.getAttribute("voice_encode_fileid")||"").replace(/^\s/,"").replace(/\s$/,"")+"_"+e.index},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return e.node.getAttribute("data-topic_id")&&e.node.getAttribute("data-topic_name")?167:122},replaceContentCssText:"",appendContentCssText:"margin-top:16px;diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mppoi",genId:function(){return(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-id")||""},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 219},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpsearch",genId:function(){return decodeURIComponent("mp-common-search")},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 100},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpvideosnap",genId:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return"live"===(e.node.getAttribute("data-type")||"video")?decodeURIComponent(e.node.getAttribute("data-noticeid")||""):decodeURIComponent(e.node.getAttribute("data-id")||"")},calW:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=e.node.getAttribute("data-type")||"video",n=e.node.getAttribute("data-width")||"",r=e.node.getAttribute("data-height")||"";if("live"===t||"topic"===t)return e.parentWidth;var i,o=1,d=0,a=!1;return 1===(o=n/r)||o===3/4||(o===4/3||o===16/9?a=!0:o<3/4?o=3/4:o>1&&o<4/3?o=1:o>4/3?a=!0:("number"!=typeof o||Object.is(o,NaN))&&(o=1)),e.node.setAttribute("data-ratio",o),e.node.setAttribute("data-isHorizontal",a),i=(d=!0===a?e.parentWidth:window.innerWidth<1024?.65*window.innerWidth:.65*e.parentWidth)/o,e.node.setAttribute("data-computedWidth",d),e.node.setAttribute("data-computedHeight",i),d},calH:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=e.node.getAttribute("data-desc")||"",n=e.node.getAttribute("data-type")||"video",r=e.node.getAttribute("data-computedHeight")||"";switch(n){case"live":return t?152:116;case"topic":return 201;case"image":case"video":return parseFloat(r)}},getBorderRadius:function(){return"video"===((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-type")||"video")?4:8},replaceContentCssText:"",appendContentCssText:"display:flex;margin:16px auto;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mp-wxaproduct",genId:function(){return decodeURIComponent((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-wxaproduct-productid")||"")},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return"mini"===((arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).node.getAttribute("data-wxaproduct-cardtype")||"")?124:466},replaceContentCssText:"",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mpprofile",genId:function(e){return e.node.getAttribute("data-id")||""},calW:function(){return 1*(arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}).parentWidth},calH:function(){return 143},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:"",outerContainerRight:""},{querySelector:"mp-common-sticker",genId:function(e){return e.node.getAttribute("data-md5")||""},calW:function(){return 120},calH:function(){return 120},replaceContentCssText:"",appendContentCssText:"diplay:block;",outerContainerLeft:'<div style="display: flex; justify-content: center;">',outerContainerRight:"</div>"}]};!function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};if("function"==typeof document.querySelectorAll)for(var t={maxWith:document.getElementById("img-content").getBoundingClientRect().width,idAttr:"data-preloadingid"},n=0,r=e.config.length;n<r;n++)for(var i=e.config[n],o=document.querySelectorAll(i.querySelector),d=0,a=o.length;d<a;d++){var c=o[d],l=c.parentNode.getBoundingClientRect().width;if(l=Math.min(l,t.maxWith),!c.getAttribute("has-insert-preloading")){var u=i.calW({parentWidth:l,node:c}),p=i.calH({parentWidth:l,node:c}),s=i.genId({index:d,node:c}),g="function"==typeof i.getBorderRadius?i.getBorderRadius({index:d,node:c}):8,h=e.defaultContentTpl.replace(/#height#/g,p).replace(/#width#/g,u).replace(/#borderRadius#/g,g),C=document.createElement("div");if(C.innerHTML=h,i.replaceContentCssText){var f=i.replaceContentCssText.replace(/#height#/g,p).replace(/#width#/g,u);C.firstChild.style.cssText=f}else i.appendContentCssText&&(C.firstChild.style.cssText+=i.appendContentCssText);var _=i.outerContainerLeft+C.innerHTML+i.outerContainerRight;C.innerHTML=_,C.firstChild.setAttribute(t.idAttr,s),c.parentNode.insertBefore(C.firstChild,c.nextSibling),c.setAttribute("has-insert-preloading","1")}}}(e)}();</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>
function htmlDecode(str) {
  return str
    .replace(/&#39;/g, '\'')
    .replace(/<br\s*(\/)?\s*>/g, '\n')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&nbsp;/g, ' ');
}

var uin = '';
var key = '';
var pass_ticket = '';
var new_appmsg = 1;
var item_show_type = "0";
var real_item_show_type = "0";
var can_see_complaint = "0";
var tid = "";
var aid = "";
var clientversion = "";
var appuin = "Mzg3NTczMDU2Mg==" || "";
var voiceid = "";
var create_time = "1643333400" * 1; // 发布时间，unix时间戳

var source = "178";
var ascene = "";
var subscene = "";
var sessionid = "" || "svr_205d18c9313";
var abtest_cookie = "";

var scene = 75;

var itemidx = "";
var appmsg_token = "";
var _copyright_stat = "1";
var _ori_article_type = "科技_互联网+";

var is_follow = "";
var nickname = "古明地觉的编程教室";
var appmsg_type = "9";
var ct = "1643333400";
var user_name = "gh_24891280c13f";
var fakeid = "";
var version = "";
var is_limit_user = "0";
var round_head_img = "http://mmbiz.qpic.cn/sz_mmbiz_png/ib8ibwulXslsEQLK5G0I0jNI3oyw7o3Vic7tA9icC88DiaRk2ozaQIG4yco1QaeLoxvgQW3W0ceDicxFmk7oTW2rZ1jw/0?wx_fmt=png";
var hd_head_img = "http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Fkmlvg8tY5dOX17y2Sm9my8HicrKaWNIsx9xbGZzOjTQ/0" || "";
var ori_head_img_url = "http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Fkmlvg8tY5dOX17y2Sm9my8HicrKaWNIsx9xbGZzOjTQ/132";
var msg_title = '《源码探秘 CPython》19. 字符集和字符编码'.html(false);
var msg_desc = htmlDecode("楔子这一次我们分析一下Python的字符串，首先字符串是一个变长对象，因为不同长度的字符串所占的内存是不一样");
var msg_cdn_url = "http://mmbiz.qpic.cn/sz_mmbiz_jpg/ib8ibwulXslsHPAO4fnichyQJPcF7VVYQv82UYZm0HeSUicM0ibImRjibSicRvvTpAkBlRsEaAz2LujORrwF6JqeticYSQ/0?wx_fmt=jpeg"; // 首图idx=0时2.35:1 ， 次图idx!=0时1:1
var cdn_url_1_1 = "https://mmbiz.qlogo.cn/sz_mmbiz_jpg/ib8ibwulXslsHPAO4fnichyQJPcF7VVYQv8VQhLX76MFlFfVSEa6QUvc9sBwc3Dy5Pia3iaQ8qRmcZ34T0994TtnzDQ/0?wx_fmt=jpeg"; // 1:1比例的封面图
var cdn_url_235_1 = "https://mmbiz.qlogo.cn/sz_mmbiz_jpg/ib8ibwulXslsHPAO4fnichyQJPcF7VVYQv82UYZm0HeSUicM0ibImRjibSicRvvTpAkBlRsEaAz2LujORrwF6JqeticYSQ/0?wx_fmt=jpeg"; // 首图idx=0时2.35:1 ， 次图idx!=0时1:1
// var msg_link = "http://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==\x26amp;mid=2247483828\x26amp;idx=1\x26amp;sn=41345986a28feb40bb7e80b985300b6f\x26amp;chksm=cf3c4259f84bcb4fa1fc9887b41b1a230980dea2a1027206e11641d4c0e3506b92464bc2b51c#rd";
var msg_link = "http://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&amp;mid=2247483828&amp;idx=1&amp;sn=41345986a28feb40bb7e80b985300b6f&amp;chksm=cf3c4259f84bcb4fa1fc9887b41b1a230980dea2a1027206e11641d4c0e3506b92464bc2b51c#rd"; // @radeonwu
var user_uin = "" * 1;
var msg_source_url = '';
var img_format = 'jpeg';
var srcid = '';
var req_id = '0313q1omzCFPsvl0AbRf3GQy';
var networkType;
var appmsgid = "" || '' || '2247483828';
var comment_id = "0" || "0" * 1;
var comment_enabled = "" * 1;
var open_fansmsg = "0" * 1;
var is_https_res = ("" * 1) && (location.protocol == "https:");
var msg_daily_idx = "1" || "";
var profileReportInfo = "" || "";

var devicetype = "";
var source_encode_biz = ""; // 转载来源的公众号encode biz
var source_username = "";
// var profile_ext_signature = "" || "";
var reprint_ticket = "";
var source_mid = "";
var source_idx = "";
var source_biz = "";
var author = "古明地觉";
var author_id = "";
var author_cancel = "" * 1 || 0;
var reward_wording = "";


// 压缩标志位
var optimizing_flag = "0" * 1;

// 广告灰度实验取消 @add by scotthuang
// var ad_abtest_padding = "0" * 1;

var show_comment = "";
var __appmsgCgiData = {
  wxa_product: "" * 1,
  wxa_cps: "" * 1,
  show_msg_voice: "0" * 1,
  can_use_page: "" * 1,
  is_wxg_stuff_uin: "0" * 1,
  card_pos: "",
  copyright_stat: "1",
  source_biz: "",
  hd_head_img: "http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Fkmlvg8tY5dOX17y2Sm9my8HicrKaWNIsx9xbGZzOjTQ/0" || (window.location.protocol + "//" + window.location.host + "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_rumor_link64f834.jpg"),
  has_red_packet_cover: "0" * 1 || 0,
  minishopCardData: ""
};
var _empty_v = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/audios/empty64f834.mp3";
var appmsg_album_info = (function () {
  var curAlbumId = '2206970536067497985';
  var publicTagInfo = [
            {
      title: 'CPython源码探秘',
      size: '91' * 1,
      link: 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&amp;action=getalbum&amp;album_id=2206970536067497985#wechat_redirect',
      type: '0' * 1,
      id: 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&amp;action=getalbum&amp;album_id=2206970536067497985#wechat_redirect' ? (('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&amp;action=getalbum&amp;album_id=2206970536067497985#wechat_redirect'.match(/[0-9]{8,}/)) ? ('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&amp;action=getalbum&amp;album_id=2206970536067497985#wechat_redirect'.match(/[0-9]{8,}/))[0] : '') : '',
      continousReadOn: '1' * 1
    },
          ];
  for (var i = 0; i < publicTagInfo.length; i++) {
    if (curAlbumId) {
      if (curAlbumId === publicTagInfo[i].id) {
        return publicTagInfo[i];
      }
    } else {
      if (publicTagInfo[i].continousReadOn) {
        return publicTagInfo[i];
      }
    }
  }
  return {};
})();
var copyright_stat = "1" * 1;
var hideSource = "" * 1;

var pay_fee = "" * 1;
var pay_timestamp = "";
var need_pay = "" * 1;
var is_pay_subscribe = "0" * 1;

var need_report_cost = "0" * 1;
var use_tx_video_player = "0" * 1;
var appmsg_fe_filter = "contenteditable";

var friend_read_source = "" || "";
var friend_read_version = "" || "";
var friend_read_class_id = "" || "";

var is_only_read = "1" * 1;
var read_num = "" * 1;
var like_num = "" * 1;
var liked = "" == 'true' ? true : false;
var is_temp_url = "" ? 1 : 0;
var tempkey = "";
var send_time = "";
var icon_emotion_switch = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/emotion/icon_emotion_switch64f834.svg";
var icon_emotion_switch_active = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/emotion/icon_emotion_switch_active64f834.svg";
var icon_emotion_switch_primary = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/emotion/icon_emotion_switch_primary64f834.svg";
var icon_emotion_switch_active_primary = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/emotion/icon_emotion_switch_active_primary64f834.svg";
var icon_loading_white = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/common/icon_loading_white64f834.gif";
var icon_audio_unread = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/audio/icon_audio_unread64f834.png";
var icon_qqmusic_default = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/audio/icon_qqmusic_default64f834.png";
var icon_qqmusic_source = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/audio/icon_qqmusic_source64f834.svg";
var icon_kugou_source = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/audio/icon_kugou_source64f834.png";

var topic_default_img = '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_book_thumb64f834.png';
var comment_edit_icon = '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/common/icon_edit64f834.png';
var comment_loading_img = '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/common/icon_loading_white64f834.gif';
var comment_c2c_not_support_img = '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_discuss_more64f834.png';

var voice_in_appmsg = {
  "1": "1"
  };
var voiceList = {};
voiceList={"voice_in_appmsg":[]}
var reprint_style = '' * 1;
var reprint_type = '' * 1;
var wxa_img_alert = "" != 'false';

// 小程序相关数据
var weapp_sn_arr_json = "" || "";

// 图文视频相关数据
var videoPageInfos = [
  ];
window.__videoPageInfos = videoPageInfos;

// 视频号相关数据
var video_snap_json = "" || "";
// profile相关数据
var mp_profile = [
  ];

// 能力封禁字段
var ban_scene = "0" * 1;

var ban_jump_link = {
    };

var svr_time = "1680498910" * 1;
// 加迁移文章字段, 默认为false
var is_transfer_msg = "" * 1 || 0;

var malicious_title_reason_id = "0" * 1; // 标题党wording id @radeonwu
var malicious_content_type = "0" * 1; // 标题党类型 @radeonwu

// 修改错别字逻辑
var modify_time = "" * 1;
var modify_detail = [];

// 限制跳转到公众号profile @radeonwu
var isprofileblock = "0";

var jumpInfo = [
    ];

var hasRelatedArticleInfo = '0' * 1 || 0; // 有相关阅读的数据 @radeonwu
var relatedArticleFlag = '' * 1 || 0; // 0不用拓展，为1时拓展3条 @yinshen

var canUseAutoTypeSetting;
canUseAutoTypeSetting = '' * 1 || 0; // 可以应用到自动排版样式
var styleType = '0';
var originTypeSetting = '';
var originStyleType = '';
var reprintEditable = '';
var currentSvrStyleType, originSvrStyleType;

if (!isNaN(parseInt(styleType)) && parseInt(styleType) > 0) {
  currentSvrStyleType = parseInt(styleType);
} else if (!isNaN(parseInt(canUseAutoTypeSetting))) {
  currentSvrStyleType = parseInt(canUseAutoTypeSetting);
} else {
  currentSvrStyleType = 0;
}

if (!isNaN(parseInt(originStyleType)) && parseInt(originStyleType) > 0) {
  originSvrStyleType = parseInt(originStyleType);
} else if (!isNaN(parseInt(originTypeSetting))) {
  originSvrStyleType = parseInt(originTypeSetting);
} else {
  originSvrStyleType = 0;
}

// 转载源段后距设置不一致 并且 转载设置为不可编辑才去修改文章段后距显示
if (reprint_type > 0 && originSvrStyleType !== currentSvrStyleType && parseInt(reprintEditable) === 0) {
  var dc = document.getElementById('js_content').classList;

  dc.remove('autoTypeSetting');
  dc.remove('autoTypeSetting24');
  dc.remove('autoTypeSetting24psection');

  var finalSetting = parseInt(originSvrStyleType); // 优先使用转载设置 做修正

  if (finalSetting === 1) {
    dc.add('autoTypeSetting');
  } else if (finalSetting === 2) {
    dc.add('autoTypeSetting24');
  } else if (finalSetting === 3) {
    dc.add('autoTypeSetting24psection');
  }
}

window.wxtoken = "777";
window.is_login = '' * 1; // 把上面的那段代码改一下，方便配置回退

window.__moon_initcallback = function () {
  if (!!window.__initCatch) {
    window.__initCatch({
      idkey: 27611 + 2,
      startKey: 0,
      limit: 128,
      badjsId: 43,
      reportOpt: {
        uin: uin,
        biz: biz,
        mid: mid,
        idx: idx,
        sn: sn
      },
      extInfo: {
        network_rate: 0.01,    //网络错误采样率
        badjs_rate: 0.1 // badjs上报叠加采样率
      }
    });
  }
}
// msg_title != title
var title = "古明地觉的编程教室";

var is_new_msg = true;
// var appmsg_like_type = "2" * 1 ? "2" * 1 : 1; //区分点赞和看一看
// var appmsg_like_type = 2;

var is_wash = '' * 1;
var topbarEnable = false;
var enterid = "" * 1 || "" * 1 || parseInt(Date.now() / 1000);
var reloadid = '' * 1 || parseInt(Date.now() / 1000); // 视频落地页连续播放id
var reloadseq = '' * 1 || 1; // 连续播放序号
// var appid_list = ""; // 改图文所在的小程序的appid列表，只在小程序中使用
var miniprogram_appid = ""; // 该图文所在的小程序的appid

var defaultAvatarUrl = '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/icon/common/icon_avatar_default64f834.svg';

document.addEventListener('DOMContentLoaded', function () {
  window.domCompleteTime = Date.now();
});

// 记录是否有转载推荐语
      var hasRecommendMsg = 0;
  ;
// 付费阅读
var isPayTopic = '' * 1;
  var payTopicPrice = '' * 1;
var isRemovedFromPayTopic = '' * 1;
var isPaySubscribe = '0' * 1; // 是否付费文章
var isPaid = '0' * 1; // 是否已付费
var isRefund = '' * 1; // 是否已退款
var payShowIAPPrice = 1; // 是否启用IAP价格显示，用于外币显示
var payProductId = '' || ''; // 付费金额对应商品ID，用于iOS多币种金额IAP查询
var previewPercent = '0' || ''; // 试读比例
var payGiftsCount = '0' * 1 || 0; // 付费赠送数量
var payDesc = htmlDecode('');
var payFreeGift = '' * 1 || 0; // 是否是领取付费赠送的用户
var is_finished_preview = 0; // 是否试读完
var jump2pay = '' * 1; // 是否跳转到支付按钮的位置

var isFans; // getext里获取数据再塞到这里
var can_reward = '0' * 1 || 0;
var is_need_reward = (isPaySubscribe && !isPaid) ? 0 : "0" * 1; // 非付费不可赞赏
var is_teenager = '' * 1 || 0; //是否处于青少年模式
var is_care_mode = '' * 1 || 0; //是否处于关怀模式

// 段落投诉
var anchor_tree_msg = '';
// Dark Mode
var colorScheme = ''; // ''|'dark'|'light', 空表示跟随系统

var iapPriceInfo = {
  };
var productPayPackage = {
    iap_price_info: iapPriceInfo
};

// 漫画原创
var isCartoonCopyright = '0' * 1; // 是否漫画原创

// 图文朗读
var show_msg_voice = '' * 1;
var qnaCardData = '';
var exptype = '' || '';
var expsessionid = '' || '';

// 留言相关
var goContentId = '';
var goReplyId = '';

var show_related_article = '' * 1; // 是否强制出相关阅读
var related_article_scene = '' * 1; // 套娃时源头文章的scene

var wwdistype = ''; // 企微场景，industrynews表示行业资讯

// 腾讯视频相关
window.cgiData = {
  appImg: '//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_tencent_video64f834.png',
}

window.show_ip_wording = '1' * 1;
window.source_appid = 'wxb3e889748b331b76'; // 公众号appid

window.is_over_sea = '' * 1; // 海外ip
</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>var __INLINE_SCRIPT__=function(){"use strict";var n=function(n,e){var i=document.getElementById("js_ip_wording_wrp"),o=document.getElementById("js_ip_wording");if(n&&(window.ip_wording={countryName:n.country_name,countryId:n.country_id,provinceName:n.province_name}),e&&e.isoversea&&(window.is_over_sea=parseInt(e.isoversea,10)),window.ip_wording&&i&&o&&1!==window.is_over_sea){var r=function(n){var e="";return 156===parseInt(n.countryId,10)?e=n.provinceName:n.countryId&&(e=n.countryName),e}(window.ip_wording);""!==r&&(o.innerHTML=r,i.style.display="inline-block")}};return window.__second_open__||(n(),window.__setIpWording=n),n}();</script><script type="text/javascript" nonce="1682091926" reportloaderror>!function(){"use strict";function e(e,t){for(var i=0;i<t.length;i++){var r=t[i];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function t(e,i){return t=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},t(e,i)}function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function r(e,t){if(t&&("object"===i(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function o(e){return o=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},o(e)}var n,a={classWhiteList:["rich_pages","blockquote_info","blockquote_biz","blockquote_other","blockquote_article","h5_image_link","img_loading","list-paddingleft-1","list-paddingleft-2","list-paddingleft-3","selectTdClass","noBorderTable","ue-table-interlace-color-single","ue-table-interlace-color-double","__bg_gif","weapp_text_link","weapp_image_link","qqmusic_area","tc","tips_global","unsupport_tips","qqmusic_wrp","appmsg_card_context","appmsg_card_active","qqmusic_bd","play_area","icon_qqmusic_switch","pic_qqmusic_default","qqmusic_thumb","access_area","qqmusic_songname","qqmusic_singername","qqmusic_source","share_audio_context","flex_context","pages_reset","share_audio_switch","icon_share_audio_switch","share_audio_info","flex_bd","share_audio_title","share_audio_tips","share_audio_progress_wrp","share_audio_progress","share_audio_progress_inner","share_audio_progress_buffer","share_audio_progress_loading","share_audio_progress_loading_inner","share_audio_progress_handle","share_audio_desc","share_audio_length_current","share_audio_length_total","video_iframe","vote_iframe","res_iframe","card_iframe","weapp_display_element","weapp_card","app_context","weapp_card_bd","weapp_card_profile","radius_avatar","weapp_card_avatar","weapp_card_nickname","weapp_card_info","weapp_card_title","weapp_card_thumb_wrp","weapp_card_ft","weapp_card_logo","pay","pay__mask","ct_geography_loc_tip","subsc_context","subsc_btn","reset_btn","icon_subsc","weui-primary-loading","weui-primary-loading__dot","wxw-img","mp-caret","appmsg_poi_iframe","cpc_iframe","channels_iframe_wrp","channels_iframe","videosnap_video_iframe","videosnap_live_iframe","videosnap_image_iframe","channels_live_iframe","minishop_iframe_wrp","minishop_iframe","mp_profile_iframe","mp_profile_iframe_wrp","mp_search_iframe_wrp","appmsg_search_iframe_wrp","appmsg_search_iframe","vote_area","vote_iframe","qqmusic_iframe","blockquote_iframe","blockquote_tips_iframe","video_iframe","shopcard_iframe","topic_iframe","weapp_app_iframe","img_fail_iframe","mp_miniprogram_iframe"],classWhiteListReg:[new RegExp("^editor__content__"),new RegExp("^wxw"),new RegExp("^js_"),new RegExp("^cps_inner"),new RegExp("^bizsvr_"),new RegExp("^code-snippet"),new RegExp("^wx_"),new RegExp("^wx-"),new RegExp("^icon_emoji_"),new RegExp("^custom_select_card")]};function s(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var i,n=o(e);if(t){var a=o(this).constructor;i=Reflect.construct(n,arguments,a)}else i=n.apply(this,arguments);return r(this,i)}}if(!window.__second_open__&&window.Darkmode){var _=0;window.Darkmode.extend([function(i){var r=!1,o=document.querySelectorAll("#js_content")[0],_=a.classWhiteList,c=a.classWhiteListReg;return window.localStorage.getItem("isMpUserAccessibility"),(null==n?void 0:n.copyright_info.is_cartoon_copyright)||null==n||n.user_info.is_care_mode,function(i){!function(e,i){if("function"!=typeof i&&null!==i)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(i&&i.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),i&&t(e,i)}(l,i);var n,a,p,m=s(l);function l(){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,l),m.apply(this,arguments)}return n=l,(a=[{key:"beforeConvertNode",value:function(e){e&&e.tagName&&("iframe"!==e.tagName.toLowerCase()?function(e){var t=e.getAttribute("class");if(t){for(var i=t.split(/\s+/),r=[],o=0,n=i.length;o<n;++o){var a=i[o];if(a&&-1!=_.indexOf(a))r.push(a);else for(var s=0,p=c.length;s<p;s++)if(c[s].test(a)){r.push(a);break}}e.setAttribute("class",r.join(" "))}}(e):"video_ad_iframe"===e.getAttribute("class")&&e.setAttribute("class",""))}},{key:"afterConvertNode",value:function(e){if(!r){var t=navigator.userAgent;/(iPhone|iPad|iPod|iOS|mac\sos)/i.test(t)&&o.classList.add("fix_apple_default_style"),r=!0}if(e.style&&""!==e.style.webkitTextSizeAdjust&&"none"!==e.style.webkitTextSizeAdjust&&(e.style.webkitTextSizeAdjust="inherit"),"animate"===e.tagName&&"height"===e.getAttribute("attributeName")){var i=e.getAttribute("repeatCount");("indefinite"===i||i>"10")&&"click"!==e.getAttribute("begin")&&"click"!==e.getAttribute("end")&&(e.setAttribute("repeatCount","undefined"),e.setAttribute("attributeName","undefined"),(new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=306525_1_1")}"OL"===e.tagName&&(e.parentNode===document.getElementById("js_content")||"js_secopen_content"===e.parentNode.getAttribute("id"))&&e.getAttribute("style")&&e.getAttribute("style").indexOf("padding-left")<0&&(e.childNodes.length>=10&&e.childNodes.length<100?(e.classList.add("extra-list-padding-level1"),e.style.paddingLeft="2.2em"):e.childNodes.length>100&&(e.classList.add("extra-list-padding-level2"),e.style.paddingLeft="3.2em"))}}])&&e(n.prototype,a),p&&e(n,p),Object.defineProperty(n,"prototype",{writable:!1}),l}(i)}]),window.Darkmode.run(document.querySelectorAll("#js_content *"),{mode:"",defaultDarkBgColor:"",error:function(){(new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_0_1"},begin:function(e){(new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_2_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_4_1"),_=1*new Date},showFirstPage:function(){_=1*new Date-_;var e=0===(document.documentElement.scrollTop||window.pageYOffset||document.body.scrollTop);_<=10?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_6_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_13_1")):_>10&&_<=20?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_7_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_14_1")):_>20&&_<=30?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_8_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_15_1")):_>30&&_<=40?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_9_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_16_1")):_>40&&_<=50?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_10_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_17_1")):_>50&&_<=60?((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_11_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_18_1")):((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_12_1",e&&((new Image).src="https://mp.weixin.qq.com/mp/jsmonitor?idkey=125617_19_1"))}}),document.getElementById("js_content").style.visibility="visible"}}();</script><script type="text/javascript" nonce="1682091926" reportloaderror>var __INLINE_SCRIPT__=function(t){"use strict";function r(t,r){var e="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!e){if(Array.isArray(t)||(e=function(t,r){if(!t)return;if("string"==typeof t)return n(t,r);var e=Object.prototype.toString.call(t).slice(8,-1);"Object"===e&&t.constructor&&(e=t.constructor.name);if("Map"===e||"Set"===e)return Array.from(t);if("Arguments"===e||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e))return n(t,r)}(t))||r&&t&&"number"==typeof t.length){e&&(t=e);var i=0,o=function(){};return{s:o,n:function(){return i>=t.length?{done:!0}:{done:!1,value:t[i++]}},e:function(t){throw t},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,u=!0,f=!1;return{s:function(){e=e.call(t)},n:function(){var t=e.next();return u=t.done,t},e:function(t){f=!0,a=t},f:function(){try{u||null==e.return||e.return()}finally{if(f)throw a}}}}function n(t,r){(null==r||r>t.length)&&(r=t.length);for(var n=0,e=new Array(r);n<r;n++)e[n]=t[n];return e}function e(t,n){if(t&&Array.isArray(t)&&n&&Array.isArray(n)){var e,o=r(t);try{for(o.s();!(e=o.n()).done;){var a=e.value,u=i(n,a.getAttribute("data-id"));if(u){var f=u.is_biz_ban,l=u.original_num,c=u.biz_account_status;a.setAttribute("data-origin_num",1*l),a.setAttribute("data-is_biz_ban",1*f),a.setAttribute("data-isban",1*f),a.setAttribute("data-biz_account_status",1*c)}}}catch(t){o.e(t)}finally{o.f()}}}function i(t,r){return t.find((function(t){return t.fakeid===r}))}function o(t,r){if(t&&r){var n=t.querySelectorAll("mp-common-profile");e(Array.from(n),function(t){var r;if(!window.__second_open__)return t;var n=(null==t||null===(r=t.biz_card)||void 0===r?void 0:r.list)||[];return n.map((function(t){return t.original_num=t.orignal_num})),n}(r))}}return window.__second_open__||o(window.document,window.mp_profile),t.updateCustomElementAttrs=o,t.updateProfileAttr=e,Object.defineProperty(t,"__esModule",{value:!0}),t}({});</script>

<script type="text/javascript" nonce="1682091926" reportloaderror>
(function(_g){
    _g.appmsg_like_type = "2" * 1 ? "2" * 1 : 1;
    // _g.appmsg_like_type = 2;
    _g.clientversion = "";
    _g.passparam = ""; // 看一看带参数
    if(!_g.msg_link) {
      _g.msg_link = "http://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&amp;mid=2247483828&amp;idx=1&amp;sn=41345986a28feb40bb7e80b985300b6f&amp;chksm=cf3c4259f84bcb4fa1fc9887b41b1a230980dea2a1027206e11641d4c0e3506b92464bc2b51c#rd";
    }
    _g.appmsg_type = "9"; // 后台图文消息类型
    _g.devicetype = ""; // devicetype
    _g.kanyikan_video_educate_pic = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_like_comment_primary64f834.png";
    _g.kanyikan_educate_pic = "//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/images/pic/pic_like_comment64f834.png";
})(window);
</script>

<script type="text/javascript" nonce="1682091926" reportloaderror>
// 企业微信里置灰公众号名称
(function() {
  var ua = window.navigator.userAgent;
  if (/MicroMessenger\/([\d\.]+)/i.test(ua) && /wxwork/i.test(ua)) {
    var profileName = document.getElementById('js_name');
    var authorName = document.getElementById('js_author_name');
    var accountNames = document.getElementsByClassName('account_nickname_inner');
    if (profileName) {
      profileName.classList.add('tips_global_primary');
    }
    if (authorName) {
      authorName.classList.add('tips_global_primary');
    }
    if (accountNames && accountNames.length) {
      accountNames[0].classList.add('tips_global_primary');
    }
  }
})();
</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>
// 安卓插入米大师 h5 sdk
(function() {
  var ua = navigator.userAgent;
  if (ua.indexOf("MicroMessenger") != -1 && ua.indexOf("Android") != -1){
    var script = document.createElement('script');
    var head = document.getElementsByTagName('head')[0];
    script.type = 'text/javascript';
    script.src = "https://midas.gtimg.cn/h5sdk/js/api/h5sdk.js";
    head.appendChild(script);
  }
})();
</script>
<script type="text/javascript" nonce="1682091926" reportloaderror>
var real_show_page_time = +new Date();
if (!!window.addEventListener){
  window.addEventListener("load", function(){
    window.onload_endtime = +new Date();
  });
}
</script>

<script nomodule nonce="1682091926" reportloaderror>new Image().src='https://mp.weixin.qq.com/mp/jsmonitor?idkey=66881_111_1&t='+Math.random();</script>

    



<script nomodule nonce="1682091926" reportloaderror>!function(){var e=document,t=e.createElement("script");if(!("noModule"in t)&&"onbeforeload"in t){var n=!1;e.addEventListener("beforeload",(function(e){if(e.target===t)n=!0;else if(!e.target.hasAttribute("nomodule")||!n)return;e.preventDefault()}),!0),t.type="module",t.src=".",e.head.appendChild(t),t.remove()}}();</script>
<script nomodule id="vite-legacy-polyfill" src="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/polyfills-legacy.666ae655.js" nonce="1682091926" reportloaderror></script>
<script nomodule id="vite-legacy-entry" data-src="//res.wx.qq.com/mmbizappmsg/zh_CN/htmledition/js/assets/appmsg-legacy.lfxjo50sae4d404e.js" nonce="1682091926" reportloaderror>System.import(document.getElementById('vite-legacy-entry').getAttribute('data-src'))</script>

  </body>
</html>
"""

str2 = """
<div>
萨达萨达hehhehe
<li></li>
<li></li>
<li></li>
</div>
"""

# cleaner = Cleaner()
# str2 = cleaner.clean_html(str2, )
# html = etree.HTML(str2)
# print(etree.tounicode(html,method="html"))

date_path = "/html/body[@id='activity-detail']/div[@id='js_article']/div[@id='js_base_container']/div[@id='page-content']/div[@class='rich_media_area_primary_inner']/div[@id='img-content']"
laji_path = "//div[@id='js_content']"
TITLE_PATH = "//h1[@id='activity-name']/text()"
html_tree = etree.HTML(str1)
article_tree = html_tree.xpath(date_path)[0]
laji_tree = article_tree.xpath(laji_path)[0]

del laji_tree.attrib["style"]
# print(etree.tounicode(laji_tree))
article = etree.tounicode(article_tree, method="html")
# print(article)
title = article_tree.xpath(TITLE_PATH)[0].strip()
print(title)

title = "test"
# with open("../templates/template.html", "r") as f:
#     new_html = f.read().format(title=title, text_date=article)
# print(new_html)
# with open("test0.html", "w", encoding="utf-8") as f:
#     f.write(new_html)
