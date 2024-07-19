<script setup lang="ts">
import { getImage } from '@/components/statics/functions.js';

</script>

<template>
  <!-- About Start -->
  <div class="container-xxl py-5">
    <div class="container">
      <!-- <div class="row g-5">
        <div class="col-lg-6 wow fadeIn" data-wow-delay="0.1s">
          <div class="d-flex flex-column">
            <img class="img-fluid align-self-end" :src="getImage('pic/helpIMG3.png')" style="width: 85%;">
            <div class="bg-dark p-4" style="margin-top: -15%; width: fit-content;">
              <h1 class="text-uppercase text-primary mb-3 fw-bold text-center">{{ $t('home_aboutPic1') }}</h1>
              <h2 class="text-uppercase mb-0 text-light fw-bold text-center">{{ $t('home_aboutPic2') }}</h2>
            </div>
          </div>
        </div>
        <div class="col-lg-6 wow fadeIn" data-wow-delay="0.5s">
          <p class="d-inline-block bg-dark text-primary py-1 px-4">{{ $t('home_about') }}</p>
          <p>{{ $t('home_about1') }}</p>
          <p>{{ $t('home_about2') }}</p>
          <p>{{ $t('home_about3') }}</p>
          <div class="row g-4">
            <div class="col-md-6">
              <h3 class="text-uppercase mb-3 text-light fw-bold">{{ $t('home_about4') }}</h3>
              <p class="mb-0">{{ $t('home_about5') }} </p>
            </div>
            <div class="col-md-6">
              <h3 class="text-uppercase mb-3 text-light fw-bold">{{ $t('home_about6') }}</h3>
              <p class="mb-0">{{ $t('home_about7') }} </p>
            </div>
          </div>
        </div>
      </div> -->
      <img class="img-fluid align-self-end" :src="getImage('pic/helpIMG3.png')">
    </div>
  </div>
  <!-- About End -->

</template>

<style scoped>
p {
  color: #ced3eb;
}
</style>