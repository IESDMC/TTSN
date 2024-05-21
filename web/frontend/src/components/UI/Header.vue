<script setup lang="ts">
import { getImage } from '@/components/statics/functions.js';
import { computed, watch } from 'vue';
import { useRoute } from 'vue-router';


//==banner
const bannerCount = 4;
const route = useRoute();
const routeName = computed(() => route.name);

//==換頁時header收起動畫重放
watch(() => routeName.value, (nV, oV) => {
  if (nV === oV) return;
  let pageHeader = document.querySelector('#pageHeader');
  if (!pageHeader) return;

  pageHeader.classList.remove('pageHeader');
  window.requestAnimationFrame(function (time) {
    window.requestAnimationFrame(function (time) {
      pageHeader.classList.add("pageHeader");
    });
  });
}, { deep: true });
// console.debug(route)
</script>

<template>
  <div class="container-fluid p-0 mb-5 wow fadeIn" data-wow-delay="0.1s">
    <!-- Carousel Start -->
    <template v-if="routeName === 'homePage'">
      <div id="header-carousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div v-for="index in Array.from(Array(bannerCount), (d, i) => i + 1)"
            :class="`carousel-item ${index === 1 ? 'active' : ''}`">
            <img class="w-100" :src="getImage(`pic/a0${index}.png`)" alt="Image">
            <div class="carousel-caption d-flex align-items-center justify-content-center text-start">
              <div class="mx-sm-5 px-5 animated" style="max-width: 900px;">
                <h3 class="mb-4 slideInDown text-light fw-bold">{{
                    $t('home_banner_title' + index)
                }}
                </h3>
                <h5 class="text-white text-uppercase mb-4 slideInDown">{{
                    $t('home_banner' + index)
                }}</h5>
              </div>
            </div>
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#header-carousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#header-carousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </template>
    <!-- Carousel End -->
    <template v-else>
      <div id="pageHeader" class="pageHeader d-flex flex-column align-items-center justify-content-center pt-0">
        <h1 v-if="routeName" class="text-uppercase display-3 mb-3 slideInDown text-light fw-bold">
          {{ $t(routeName.toString()) }}
        </h1>
      </div>

      <!-- <div class="d-flex flex-column align-items-center justify-content-center pt-0 pt-lg-5" data-v-ca863e68=""
        style="min-height: 400px;">
        <h1 class="display-4 mb-3 mt-0 mt-lg-5 text-white text-uppercase" data-v-ca863e68="">Event Data</h1>
        <div class="d-inline-flex mb-lg-5" data-v-ca863e68="">
          <p class="m-0 text-white size" data-v-ca863e68="">Waveform</p>
          <div class="m-0 text-white source" data-v-ca863e68="">Source:USGS</div>
        </div>
      </div> -->
    </template>
  </div>



</template>

<style scoped>
/*** Header ***/
.carousel-caption {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.carousel-control-prev,
.carousel-control-next {
  width: 10%;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  width: 3rem;
  height: 3rem;
}

@media (max-width: 768px) {
  #header-carousel .carousel-item {
    position: relative;
    min-height: 450px;
  }

  #header-carousel .carousel-item img {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

#header-carousel .carousel-item .animated {
  position: absolute;
  left: 10%;
  bottom: 10%;
  /* white-space: pre; */
}

.pageHeader {
  background-size: cover;
  min-height: 200px;
  background-image: linear-gradient(rgba(0, 0, 0, .85), rgba(0, 0, 0, .55)), url('@/assets/img/pic/p-alert_DM_CH.png');
  animation: hideHeader 2s ease 1s forwards;
}

.pageHeader>h1 {
  animation: hideHeaderText 1s ease 1.5s forwards;
}

@keyframes hideHeader {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    min-height: 0px;
  }
}

@keyframes hideHeaderText {
  0% {}

  60% {
    font-size: 0;
  }

  100% {
    font-size: 0;
  }
}
</style>