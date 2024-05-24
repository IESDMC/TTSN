<script setup lang="ts">
import Footer from "@/components/UI/Footer.vue";
import { useVueLoaderStore } from "@/stores/vueLoader";
import { useI18n } from 'vue-i18n';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';
import { RouterView } from 'vue-router';

//==i18n
const { locale } = useI18n();
const lang = ['tw', 'en'];
let langIdx = 1;
const handleChangeLanguage = (e) => {
  langIdx = +!langIdx;
  locale.value = lang[langIdx];
};

//==VueLoader
const VueLoaderStore = useVueLoaderStore();

</script>

<template>
  <!-- Nav Start -->
  <nav class="navbar navbar-expand-lg py-lg-0 px-lg-5 border-bottom shadow-sm fadeIn" data-wow-delay="0.1s">
    <a class="navbar-brand ms-4 ms-lg-0">
      <h3 class="mb-0 text-dark fw-bold">
        TTSN<small> - paper seismogram scec data center</small>
      </h3>
      <p>Taiwan Telemetered Seismographic Network</p>
    </a>
    <button type="button" class="navbar-toggler me-4" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse navbar-nav p-lg-0 justify-content-lg-end" id="navbarCollapse">
      <router-link class="nav-item nav-link" to="/">{{ $t('homePage') }}</router-link>
      <router-link class="nav-item nav-link" to="/station">{{ $t('stationPage') }}</router-link>
      <router-link class="nav-item nav-link" to="/data">{{ $t('dataPage') }}</router-link>
      <router-link class="nav-item nav-link" to="/help">{{ $t('helpPage') }}</router-link>
      <!-- <router-link class="nav-item nav-link" to="/publications">{{ $t('publicationsPage') }}</router-link> -->
      <span class="nav-item nav-link">|</span>
      <a class="nav-item nav-link" @click="handleChangeLanguage">
        {{ $t('langTag') }}
      </a>
    </div>
  </nav>
  <!-- Nav End -->
  <div class="container-fluid p-0 mb-5">
    <Header />
  </div>
  <div class="RouterView m-3">
    <RouterView />
  </div>
  <div class="container-fluid p-0 mt-5">
    <Footer />
  </div>
  <loading :active="VueLoaderStore.loaderActive" is-full-page="true" loader="bars" width="100" height="100"
    background-color="#fff" />
</template>

<style lang="scss">
:root {
  --primary: #eb1616;
  --dark: #000000;
  --light: #6c7293;
  --secondary: #89c3eb;
  --blue: #ebf6f7;
}

.text-primary {
  color: var(--primary) !important;
}

body {
  // background-color: var(--dark) !important;
  font-family: "Oswald", sans-serif;

  .RouterView {
    position: relative;
    z-index: 999;
  }
}



/*** Navbar ***/
.navbar {
  background-color: var(--blue);
  border-bottom: 1px solid var(--secondary);
  color: var(--dark);

  .dropdown-toggle::after {
    border: none;
    content: "\f107";
    font-family: "Font Awesome 5 Free";
    font-weight: 900;
    vertical-align: middle;
    margin-left: 8px;
  }

  .navbar-nav .nav-link {
    margin-right: 30px;
    padding: 20px 0;
    // color: var(--light);
    font-family: "Oswald", sans-serif;
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    outline: none;
    white-space: nowrap;

    .active,
    &:hover {
      color: var(--light) !important;
    }
  }
}



@media (max-width: 991.98px) {

  .navbar .navbar-nav .nav-link,
  .navbar.shadow-sm .navbar-nav .nav-link {
    margin-right: 0;
    padding: 10px 0;
  }

  .navbar .navbar-nav {
    margin-top: 8px;
    border-top: 1px solid var(--light);
  }
}

@media (min-width: 992px) {
  .navbar-expand-lg .navbar-collapse {
    display: flex !important;
    flex-basis: auto;
  }


  .navbar.shadow-sm .navbar-nav .nav-link {
    padding: 20px 0;
  }


  .navbar .nav-item .dropdown-menu {
    display: block;
    border: none;
    margin-top: 0;
    top: 150%;
    opacity: 0;
    visibility: hidden;
    transition: 0.5s;
  }

  .navbar .nav-item:hover .dropdown-menu {
    top: 80%;
    visibility: visible;
    transition: 0.5s;
    opacity: 1;
  }

  .navbar .nav-item .dropdown-menu a:active,
  .navbar .nav-item .dropdown-menu .router-link-active {
    color: #fff !important;
    background-color: var(--primary);

  }
}
</style>
