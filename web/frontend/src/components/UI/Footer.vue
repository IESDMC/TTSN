<script setup lang="ts">
import { getImage } from '@/components/statics/functions.js';
</script>

<template>
  <!-- Footer Start -->
  <div class="footer wow fadeIn" data-wow-delay="0.1s">
    <div class="container py-5">
      <div class="row g-5">
        <div class="col-lg-6 col-sm-12">
          <h4 class="text-uppercase mb-4 fw-bold">{{ $t('getInTouch') }}</h4>
          <div class="d-flex align-items-center mb-2">
            <div class="btn-square flex-shrink-0 me-3">
              <span class="fa fa-map-marker-alt"></span>
            </div>
            <span>{{ $t('getInTouch_location') }}</span>
          </div>
          <div class="d-flex align-items-center mb-2">
            <div class="btn-square flex-shrink-0 me-3">
              <span class="fa fa-phone-alt"></span>
            </div>
            <span>{{ $t('getInTouch_tel') }}</span>
          </div>
          <div class="d-flex align-items-center">
            <div class="btn-square flex-shrink-0 me-3">
              <span class="fa fa-envelope-open"></span>
            </div>
            <span>{{ $t('getInTouch_email') }}</span>
          </div>
        </div>
        <div class="col-lg-6 col-sm-12 d-flex flex-column align-items-center">
          <a href="https://www.nstc.gov.tw/?l=en" target="_blank">
            <div class="picture">
              <img :src="getImage('logo/nstc.09fc84ba.png')" class="pt-2 px-1">
            </div>
          </a>
          <a href="https://www.earth.sinica.edu.tw/?lang=en" target="_blank">
            <div class="picture">
              <img :src="getImage('logo/logo_ies.698a0be8.png')" class="pt-1 px-1">
            </div>
          </a>
          <!-- <a href="http://www.gl.ntu.edu.tw/index.php" target="_blank">
            <div class="picture">
              <img :src="getImage('logo/logo_type2.gif')" class="pt-2 ps-1">
            </div>
          </a> -->
        </div>
      </div>
    </div>
    <div class="container">
      <div class="copyright">
        <div class="row">
          <div class="col-md-6 text-center text-md-start mb-3 mb-md-0">
            &copy; <a class="border-bottom" href="https://dmc.earth.sinica.edu.tw/" target="_blank">DMC, IESAS</a>, All
            Right Reserved.
          </div>

          <!--/*** This template is free as long as you keep the footer author’s credit link/attribution link/backlink. If you'd like to use the template without the footer author’s credit link/attribution link/backlink, you can purchase the Credit Removal License from "https://htmlcodex.com/credit-removal". Thank you for your support. ***/-->
          <!-- <div class="col-md-6 text-center text-md-end">
            Designed By <a class="border-bottom" href="https://htmlcodex.com" target="_blank">HTML Codex</a>
          </div> -->

        </div>
      </div>
    </div>
  </div>
  <!-- Footer End -->


  <!-- Back to Top -->
  <a href="#" class="btn btn-primary btn-lg-square back-to-top"><i class="fa-solid fa-arrow-up"></i></a>
</template>

<style lang="scss" scoped>
/*** Footer ***/
.footer {
  background-color: var(--blue);
  border-bottom: 1px solid var(--secondary);
  color: var(--dark);

  .btn.btn-link {
    display: block;
    margin-bottom: 5px;
    padding: 0;
    text-align: left;
    color: var(--light);
    font-size: 15px;
    font-weight: normal;
    text-transform: capitalize;
    transition: 0.3s;

    &::before {
      position: relative;
      content: "\f105";
      font-family: "Font Awesome 5 Free";
      font-weight: 900;
      margin-right: 10px;
    }

    &:hover {
      color: var(--primary);
      letter-spacing: 1px;
      box-shadow: none;
    }

  }

  .copyright {
    padding: 1.5rem;
    font-size: 15px;
    background: var(--secondary);

    a {
      color: var(--light);

      &:hover {
        color: var(--primary);
      }

    }

  }

  .btn-square {
    width: 38px;
    height: 38px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: normal;
    background-color: var(--secondary);

    .fa {
      color: var(--light);
    }
  }

  .picture {
    position: relative;
    width: 310px;
    top: 10px;
    left: 5px;
    margin: 10px;
    height: 70px;
    background-color: var(--light);

    img {
      position: absolute;
      width: 300px;
    }
  }

}

.back-to-top {
  position: fixed;
  display: none;
  right: 45px;
  bottom: 45px;
  z-index: 99;
}
</style>