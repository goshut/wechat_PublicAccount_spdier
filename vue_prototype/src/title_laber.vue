<script setup>
const props = defineProps(['index', "title", "a_click"])
</script>

<template>
    <li class="chapter li_laber" data-level="0.1">
        <a v-bind:title="title" @click="a_click($event)">
            <b>{{ index + 1 }}.</b>
            {{ title }}
        </a>
    </li>
</template>

<style scoped>
/* ................这玩意也有作用域的概念 */
.active_title_laber {
    padding: 5px;
    /* margin: 5px; */
    color: #008cff;
    /* 文字颜色 */
    background: #ffec8b;
    /* 背景颜色 */
    /* padding: 5px 10px; */
    /* 内边距：上下5px，左右10px */
    border-radius: 20px;
    /* 圆角边框 */
    /* border: 1px solid #008cff; */
    /* 边框颜色和样式 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    /* 阴影效果 */
    /* text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); */
    /* 文字阴影，增加可读性 */
    transition: all 0.3s ease;
    /* 过渡效果，使状态变化更平滑 */
}

/* 鼠标悬停时的样式 */
/* .active_title_laber:hover { */
/* background: #ffec8b; */
/* text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); */
/* 鼠标悬停时的背景颜色变化 */
/* color: #0056b3; */
/* 鼠标悬停时的文字颜色变化 */
/* transform: scale(1.05); */
/* 轻微放大效果，增加交互感 */
/* } */

.li_laber {
    padding: 5px 10px;
}

a {
    cursor: pointer;
}

/* 为了防止忘记.. */
.book .book-summary ul.summary li a,
.book .book-summary ul.summary li span {
    display: block;
    padding: 5px 5px;
    border-bottom: none;
    /* color: #364149; */
    /* background: 0 0; */
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    position: relative
}

.book .book-summary ul.summary li a:hover,
.book .book-summary ul.summary li.active>a {
    color: #008cff;
    /* background: 0 0; */
    text-decoration: none
}
</style>
