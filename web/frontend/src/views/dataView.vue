<script setup lang="ts">
import dataTableUI from "@/components/UI/dataTableUI.vue";
import dialogUI from "@/components/UI/dialogUI.vue";
import mapControllerUI from "@/components/UI/mapControllerUI.vue";
import type { UIControlsType } from "@/components/statics/types";
import stationsMap from "@/components/stationsMap.vue";
import { reactive, ref } from "vue";

const dataList = ref();
const mapController = ref();
const theme = ref('black');

const changeDataList = (list: any[]) => {
  dataList.value = list;
};
const getMapController = (c: any[]) => {
  mapController.value = c;
};

const UIControls: UIControlsType = {
  tableTarget: reactive({
    hovered: undefined,
    clicked: undefined,
    type: "data",
    action: 'download',
    // selectFlag: true,//用於選擇列表
  }),
  dialogUI: reactive({
    openState: false,
    maxWidth: 0,
    content: {
      type: '',
      data: undefined,
    },
  }),
  others: reactive({
    tableAllStaTotal: 0,
    mapExpand: false
  }),
};

</script>

<template>
  <div class="row" v-for="mapExpand in [UIControls.others?.mapExpand]">

    <div :class="`mapView  ${mapExpand ? 'col-lg-6' : 'd-none'}`">
      <stationsMap :UIControls="UIControls" :isDataView="true" @changeDataList="changeDataList"
        @getMapController="getMapController" />
    </div>

    <div :class="`tableView col-12 ${mapExpand ? 'col-lg-6' : ''}`">
      <dataTableUI :dataList="dataList" :UIControls="UIControls" />
    </div>

    <div v-if="!!mapController" :class="`controller-wrapper ${mapExpand ? '' : 'ctrlBlur'}`"
      :style="{ position: mapExpand ? 'absolute' : 'sticky' }">
      <mapControllerUI :mapController="mapController" :theme="theme">
      </mapControllerUI>
    </div>

    <dialogUI :dialogControls="UIControls.dialogUI"></dialogUI>
  </div>
</template>
<!-- :style="{ position: mapExpand ? 'absolute' : 'sticky' }" -->
<style lang="scss" scoped>
.controller-wrapper {
  --blur-opacity: 0.5;
  z-index: 5;
  bottom: 5%;

  &.ctrlBlur {
    :deep(.toolbar) {
      border: 2px solid rgba(0, 0, 0, var(--blur-opacity));

      &:hover {
        border: 2px solid rgba(0, 0, 0, 1);
      }

      img.button {
        opacity: var(--blur-opacity);

        &:hover {
          opacity: 1;
        }
      }
    }
  }

}
</style>
