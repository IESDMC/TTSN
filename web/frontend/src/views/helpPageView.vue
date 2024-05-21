<script setup lang="ts">
import { getImage } from '@/components/statics/functions.js';
import { computed } from 'vue';
import { useI18n } from "vue-i18n";
import { useRoute } from 'vue-router';

const pageName = computed(() => useRoute().params.page);
const { locale } = useI18n();

function fixImgSrc(rawText) {
  const regex = /<img[^>]*\bsrc=['"]([^'"]*)['"][^>]*>/g;
  const newText = rawText.replaceAll(regex, (match, srcValue) => {
    // console.debug(match, srcValue);
    // 在这里进行替换操作，例如替换成新的 src 值
    return match.replace(srcValue, getImage(srcValue));
  });


  return newText;
};
function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  const navBar = document.querySelector('nav');

  if (element) {
    const offset = -navBar.clientHeight; // 上方偏移 50 像素
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.scrollY + offset;

    // 延遲 100 毫秒後再執行滾動
    setTimeout(function () {
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }, 100);

    // console.debug(elementId, offset)
  }
};
</script>

<template >
  <div class="container">
    <div class="contents d-flex flex-column w-50">
      <a href="javascript:void(0);" @click="scrollToElement('resultPage_help')">
        {{ $t('resultPage') }}
      </a>
      <a href="javascript:void(0);" @click="scrollToElement('modelPage_help')">
        {{ $t('modelPage') }}
      </a>

      <!-- <a href="#resultPage_help" class="">{{ $t('resultPage_help') }}</a>
    <a href="#modelPage_help" class="">{{ $t('modelPage_help') }}</a> -->
    </div>

    <div class="my-4">
      <!-- <h1 class="fw-bold">{{ $t('helpPage') }}</h1> -->
      <p class="h4 my-4">{{ $t('introduction_help') }}</p>
    </div>

    <div class="border-bottom my-4" id="resultPage_help">
      <h1 class="fw-bold">{{ $t('resultPage') }}</h1>
      <p class="h4 my-4" v-html="fixImgSrc($t('resultPage_help1'))"></p>
      <div class="d-flex flex-column align-items-center">
        <img class="helpIMG" :src="getImage(`pic/helpIMG1.png`)" />
        <span class="">{{ $t('resultPage_helpIMG1') }}</span>
      </div>
    </div>

    <div class="border-bottom my-4" id="modelPage_help">
      <h1 class="fw-bold">{{ $t('modelPage') }}</h1>
      <p class="h4 my-4" v-html="fixImgSrc($t('modelPage_help1'))"></p>
      <div class="d-flex flex-column align-items-center">
        <img class="helpIMG" :src="getImage(`pic/helpIMG2.png`)" />
        <span class="">{{ $t('modelPage_helpIMG1') }}</span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@keyframes linkBlink {
  0% {
    background: false;

  }

  100% {
    color: #00cdd0;
    background: rgb(0, 205, 208, 0.3);
  }
}

.contents {
  background-color: #272726;
  border-radius: 3px;

  a {
    text-decoration: none;
    font-size: 1.5rem;
    padding: 0.75rem 1.25rem;
    color: white;

    &:hover {
      animation: linkBlink 0.1s linear forwards;
    }

  }

}

:deep(p>img) {
  padding: 3px;
  border-radius: 6px;
  background: #06d85f;
  width: 30px;
  height: 30px;
}

.helpIMG {
  max-width: 80%;
}

// #resultPage_help {
//   margin-top: -50px;
//   padding-top: 50px;
//   /* 避免跳轉後元素被遮擋 */
// }
</style>
