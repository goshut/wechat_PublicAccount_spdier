<script setup>
import { ref, computed, onMounted } from 'vue';
import title_laber from './title_laber.vue';
// 获取所有 dir_message 标签的元素集合
const dir_messages = document.getElementsByTagName("dir_message");
const page_title = document.title
let old_active_laber = undefined
const active_title = ref(null)
// 定义一个 computed 属性 article_url
const article_url = computed(() => {
  // 如果 active_title 有值，就返回 active_title + ".html"
  // 否则就返回空字符串
  return active_title.value ? active_title.value + ".html" : ""
})
// 不需要那麽多花里胡哨的操作...iframe不受控,就在iframe页面写好了..
// 代码就不删了,知道和它通讯的方法就好了


// let iframe = undefined;
// let doc = undefined;
// let iframeWindow = undefined; // 暂时用不到了,它是在有服务器的情况下不通过传消息获取iframe信息用的
// console.log()
// 遍历集合并打印每个元素的内容
// for (var i = 0; i < dir_messages.length; i++) {
//   console.log(dir_messages[i].innerText); // 或者 messages[i].innerHTML
// }
function a_click(event) {
  // this event这2货貌似是全局变量,不需要传参..
  const laber = event.target
  // console.log(event)
  // console.log(this)
  // console.log(laber)
  if (laber !== old_active_laber) {
    active_title.value = this.title
    laber.classList.add('active_title_laber')
    if (old_active_laber) {
      old_active_laber.classList.remove('active_title_laber')
      // save_wind_offset()
      // save_wind_offset(old_active_laber.title)
    }
    old_active_laber = laber
  }
}
// function save_wind_offset() {
  // 获取滚动位置
  // const iframe = document.getElementById('_iframe');
  // iframeWindow = iframe.contentWindow || iframe.contentDocument.defaultView;
  // 并不能使用常规方法获取到 file:/// 协议下的iframe页面数据
  // const scrollPosition = iframe.contentDocument.documentElement.scrollTop;
  // // alert(scrollPosition)
  // // console.log(scrollPosition)
  // localStorage.setItem(wind_key, scrollPosition);

  // 向iframe发送保存消息
//   iframe.contentWindow.postMessage('save_scroll_position', "*")
// }
// 监听来自 <iframe> 的响应
// window.addEventListener('message', event => {
//   alert("收到了: " + event.origin + "-->>" + event.data)
//   console.log("main:")
//   console.log(event.data)
//   console.log(event.origin)
//   console.log(event.source)
//   // 确保事件来源是你的 <iframe>
//   if (event.origin === 'http://你的iframe域名') {
//     console.log('Received scroll position from iframe:', event.data);
//   }

// });
// function scrollToPosition() {
//   iframe = document.getElementById('_iframe');
//   doc = iframe.contentDocument || iframe.contentWindow.document;
//   // 获取要滚动的位置
//   const offset = JSON.parse(localStorage.getItem(active_title.value + "_scroll_position"))
//   // 滚动到指定位置，这里的100是示例值，代表垂直滚动的像素数
//   // console.log("要滚动的位置: ", offset)
//   // doc.documentElement.scrollX是只读的
//   if (offset) {
//     doc.documentElement.scrollTo(offset.scrollX, offset.scrollY);
//     doc.body.scrollTo(offset.scrollX, offset.scrollY); // 对于某些浏览器，可能需要这种方式
//   }
// }
// onMounted(async () => {
//   // 这样写不太行...新打开的iframe被视为新的object...
//   iframe = document.getElementById('_iframe');
//   doc = iframe.contentDocument || iframe.contentWindow.document;
//   iframeWindow = iframe.contentWindow || iframe.contentDocument.defaultView;
// })



</script>

<template>
  <!-- <script type="module">
      const {createApp} = Vue
      createApp({
          data() {
              return {
                  article_url: "",
                  select_sign: '0',
              }
          },
          methods: {
              change_article_url(e, select_sign) {
                  this.article_url = e.currentTarget.id
                  this.select_sign = select_sign
              }
          },

      }).mount('#app')
    </script> -->


  <div class="book-summary">
    <ul class="summary">
      <li class="chapter active" data-level="0" data-path="index.html">
        <a id="page_title" class=active_title_laber>
          {{ page_title }}
        </a>
      </li>


      <div v-for="(message, index) in dir_messages" :key="index">
        <title_laber :title="message.innerText" :index="index" :a_click="a_click"></title_laber>
      </div>



    </ul>
  </div>
  <div class="book-body iframe_div">
    <!-- 巨坑点,js绑定时要加fun(),表示调用函数, vue中 :简写绑定而且不能加()因为它绑定一个变量,此时此标签它还没被渲染出来 -->
    <iframe id="_iframe" :src="article_url" width="100%" height="100%" frameborder="no"
      :onload="scrollToPosition"></iframe>
  </div>
</template>

<style scoped>
/* ................这玩意也有作用域的概念 */
/* 通过 id 选择器设置 a 标签的样式 */
#page_title {
  color: lightgreen;
  /* 设置文字颜色为绿色 */
  font-weight: bold;
  /* 设置文字加粗 */
  text-decoration: none;
  /* 去除下划线 */
  text-align: center;
  font-size: 24px;
  /* 设置文字大小为 24px */
  margin: 0 auto;
  /* 设置水平方向上的外边距为自动 */
}

.iframe_div {
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中（如果需要） */
  height: 100%;
  /* 确保父容器有足够的高度 */
}

#_iframe {
  display: block;
  /* 使iframe表现为块级元素 */
  margin: 0 auto;
  /* 上下边距为0，左右自动调整实现居中 */
  /* padding: 15%; */
}
</style>
