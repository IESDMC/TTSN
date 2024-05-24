<script setup lang="ts">
import type { dialogUIType } from "@/components/statics/types";
// import { useAuthStore } from "@/stores/authStore";
import { useDataFileStore } from "@/stores/getDataFile";
import { GDialog } from 'gitart-vue-dialog';
import 'gitart-vue-dialog/dist/style.css';
import { storeToRefs } from "pinia";
import { onMounted, watch, type PropType } from "vue";

const dataFileStore = useDataFileStore();
const { fileData } = storeToRefs(dataFileStore);
const props = defineProps({
  dialogControls: {
    type: Object as PropType<dialogUIType>,
    default: null,
    required: false,
  },
});
const dialogControls = props.dialogControls;



onMounted(() => {
  //==根據要呈現內容取得資料
  watch(dialogControls.content, async (content) => {
    // console.debug(content);
    dataFileStore.resetState();

    let type = content.type,
      data = content.data;

    let maxWidth = window.innerWidth * 0.8;
    switch (type) {
      // case 'downloadForm':
      //   maxWidth = 800;
      //   break;
      case 'scanView':
        let params = {
          year: data.date.split('-')[0],
          fileName: data.fileName,
        };

        await dataFileStore.getImgFile(0, [data]);
        break;
      // default:
      //   let typeIdx = {
      //     'polarPlot': 2,
      //     'scatterPlot1': 3,
      //     'gif1': 4,
      //     'gif2': 5,
      //     'gif3': 6,
      //     'scatterPlot2': 7,
      //     'pgaPlot': 8,
      //   }[type];
      //   dataFileStore.getEventFiles(data.event, typeIdx);
      //   maxWidth = 800;
      //   break;
    };

    Object.assign(dialogControls, {
      openState: true,
      maxWidth,
    });

  }, { deep: true });
});
</script>

<template>
  <GDialog v-model="dialogControls.openState" :max-width="dialogControls.maxWidth">
    <div class="wrapper">
      <div class="content">
        <!-- x icon-->
        <button type="button" class="close">
          <span aria-hidden="true" @click="dialogControls.openState = false">&times;</span>
        </button>
        <div class="title">{{ $t(dialogControls.content.type) }}</div>
        <template v-if="fileData">
          <div class="subTitle">
            {{ `${$t('date')} : ${dialogControls.content.data.date} / \
            ${$t('station')} : ${dialogControls.content.data.station} / \
            ${$t('component')} : ${dialogControls.content.data.component}` }}
          </div>
          <div class="graphics container d-flex align-items-center justify-content-center">
            <img :src="fileData.data" @click="fileData.onClick" />
          </div>
        </template>
      </div>
    </div>
  </GDialog>
</template>

<style>
.g-dialog-overlay {
  z-index: 2000 !important;
}

.g-dialog-frame {
  z-index: 3000 !important;
}
</style>

<style lang="scss" scoped>
.wrapper {
  color: #000;

  .content {
    padding: 20px;

    .title {
      font-size: 30px;
      font-weight: 700;
      margin-bottom: 10px;
      text-align: center;
    }

    .subTitle {
      font-size: 20px;
      margin-bottom: 5px;
      text-align: center;
    }

    button {
      &.close {
        padding: 0;
        background-color: transparent;
        border: 0;
        float: right;
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1;
        color: #000;
        text-shadow: 0 1px 0 #fff;
        opacity: 0.5;

        &:hover {
          color: #06d85f;
        }

      }
    }


  }

}

.graphics {
  img {
    &:hover {
      cursor: zoom-in;
    }

    width: 100%;
  }

  div {
    width: 100%;
  }
}
</style>

<!-- 圖表相關css -->
<style lang="scss" scoped>
/* tooltop,nav-menu...通用css */
:deep(.graphics) {

  text,
  label,
  a,
  option {
    user-select: none;
  }

  .toggle-menu {
    position: absolute;
    right: 0;

    ul {
      width: 200px;
      height: 200px;
      position: absolute;
      top: 100%;
      right: 0px;
      padding: 0px 0px 0px 0px;
      box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.15);
      border: rgb(197, 197, 197) 1px solid;
      border-radius: 3px;
      background-color: #fff;
    }

    li {
      float: none;
      display: block;

      a {
        text-decoration: none;
        color: #777;
        text-align: center;
        font-size: 16px;

        &:hover {
          background: #1abc9c;
          color: #fff;
        }
      }

    }


    .toggle-nav {
      padding: 5px 9px 5px 10px;
      display: inline-block;
      box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.15);
      border: rgb(197, 197, 197) 1px solid;
      border-radius: 3px;
      text-shadow: 0px 1px 0px rgba(0, 0, 0, 0.5);
      color: #777;
      font-size: 20px;
      text-decoration: none;

      &:hover,
      &.show {
        color: rgba(0, 0, 0, 0.658);
      }

    }
  }

  .dropdown-menu {
    padding: 10px 20px;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .grid .tick {
    stroke: lightgrey;
    opacity: 0.7;
  }

  .tooltip {
    position: absolute;
    z-index: 999;
    background-color: #d3d3d3;
    padding: 20px 20px 20px 20px;
    opacity: 0.9;
    display: none;
    pointer-events: none;
    white-space: nowrap;
  }
}

/* DistxWave css*/
:deep(.graphics>#travelTimeCurve) {
  --w: 150px;
  --list-length: 4;
  --sidePadding: 2px;

  #NSRange {
    width: var(--w);
  }

  #NSList {
    display: block;
    margin-top: -10px;

    option {
      display: inline-block;
      width: calc((var(--w) - var(--sidePadding)) / ((var(--list-length) - 1)));
      text-align: center;
      text-anchor: middle;

      /* alignment-baseline: text-before-edge; */
      // font-weight: bold;

      /* font-size: 100; */
      &:first-child {
        width: calc((var(--w) - var(--sidePadding)) / ((var(--list-length) - 1) * 2));
        text-align: left;
        padding-left: 3px;
      }

      &:last-child {
        width: calc((var(--w) - var(--sidePadding)) / ((var(--list-length) - 1) * 2));
        text-align: right;
        padding-left: 12px;
      }
    }
  }

  #xAxisName_radioGroup {
    input[name="xAxisRange"] {
      max-width: 40%;
    }

    .dropdown-menu {
      left: auto;
      right: 0;
      top: 100%;
    }
  }

  .slider-handle {
    --slider-handle-width: 16px;
    width: var(--slider-handle-width);
    height: var(--slider-handle-width);
    margin-top: calc(10px - var(--slider-handle-width) * 0.5);
  }

  .slider-selection {
    background: #0480be;
  }

  .slider-track {
    border-color: #afafafb9;
    border-style: solid;
    border-width: 1px;
  }

  #displayMenu {
    max-width: 220px;
  }

  #channelMenu {
    max-width: 180px;
  }

  #chartMain {
    position: relative;
  }

  #loading {
    --loading-width: 150px;
    --loading-height: 60px;

    position: absolute;
    width: var(--loading-width);
    height: var(--loading-height);
    left: calc(50% - var(--loading-width) * 0.5);
    top: calc(50% - var(--loading-height));
    z-index: 50;
    padding: 10px 10px;
    background: #3c3c3c;
    color: #fff;
    text-align: center;
    box-shadow: 2px 2px 10px;
    border-radius: 5px;
  }
}

/* sacPlot css*/
:deep(.graphics>#sacPlot) {
  .yAxis .domain {
    stroke: none;
  }

  .chart {
    position: relative;
    padding: 10px 15px;
  }
}
</style>
