<script setup lang="ts">
import type { UIControlsType } from "@/components/statics/types";
import stationsMap from "@/components/stationsMap.vue";
import dataTableUI from "@/components/UI/dataTableUI.vue";
import { reactive, ref } from "vue";

const dataList = ref();
const changeDataList = (list: any[]) => {
  dataList.value = list;
};

const UIControls: UIControlsType = {
  tableTarget: reactive({
    hovered: undefined,
    clicked: undefined,
    type: "station",
  }),
  others: reactive({
    tableAllStaTotal: 0,
    mapExpand: false
  }),
  // dialogUI: reactive({
  //   openState: false,
  // }),
};

</script>

<template>
  <div class="row" v-for="mapExpand in [UIControls.others?.mapExpand]">
    <div :class="`mapView col-12 ${mapExpand ? '' : 'col-lg-6'}`">
      <stationsMap :UIControls="UIControls" @changeDataList="changeDataList" />
    </div>
    <div :class="`tableView col-12 ${mapExpand ? '' : 'col-lg-6'}`">
      <dataTableUI :dataList="dataList" :UIControls="UIControls" />
    </div>
  </div>
</template>

<style scoped>
.mapView {
  position: relative;
  z-index: 1;
}
</style>
