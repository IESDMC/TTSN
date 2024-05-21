<script setup lang="ts">
import { getImage } from '@/components/statics/functions.js';
import type { mapControllerType } from "@/components/statics/types";
import L from "leaflet";
import MultiRangeSlider from 'multi-range-slider-vue';
import "multi-range-slider-vue/MultiRangeSliderBarOnly.css";
import { onMounted, onUnmounted, watch, type PropType } from 'vue';
import { useI18n } from 'vue-i18n';


const { t } = useI18n({ inheritLocale: true });

const props = defineProps({
  mapController: {
    type: Object as PropType<mapControllerType>,
    required: true,
  },
  theme: {
    type: String,
    required: true,
  },
});

const icons = props.mapController.icons,
  mapName: string = props.mapController.mapName;
const criteria = icons.criteria?.popup,
  display = icons.display?.popup,
  graphics = icons.graphics?.popup,
  legend = display?.legend;

const iconBtns: typeof icons = {
  notToAutoClose: ["lockView", "expand"],
  get criteria() {
    return icons.hasOwnProperty('criteria') ? {
      hotkey: "C",
      img: "criteria",
      onclick: () => {
        let flag = !icons.criteria.flag;
        if (flag)
          Object.keys(icons)
            .filter(key => !iconBtns.notToAutoClose.includes(key))
            .forEach(key => icons[key].flag = false);
        icons.criteria.flag = flag;
      }
    } : false;
  },
  get display() {
    return icons.hasOwnProperty('display') ? {
      hotkey: "S",
      img: "display",
      onclick: () => {
        let flag = !icons.display.flag;
        if (flag)
          Object.keys(icons)
            .filter(key => !iconBtns.notToAutoClose.includes(key))
            .forEach(key => icons[key].flag = false);
        icons.display.flag = flag;
      }
    } : false;
  },
  get lockView() {
    return icons.hasOwnProperty('lockView') ? {
      hotkey: "L",
      img: icons.lockView.flag ? "unlockView" : "lockView",
      onclick: () => {
        icons.lockView.flag = !icons.lockView.flag;
        iconBtns.lockView.img = icons.lockView.flag ? "unlockView" : "lockView";
      }
    } : false;
  },
  get graphics() {
    return icons.hasOwnProperty('graphics') ? {
      hotkey: "G",
      img: "graphics",
      onclick: () => {
        let flag = !icons.graphics.flag;
        if (flag)
          Object.keys(icons)
            .filter(key => !iconBtns.notToAutoClose.includes(key))
            .forEach(key => icons[key].flag = false);
        icons.graphics.flag = flag;
      }
    } : false;
  },
  get expand() {
    return icons.hasOwnProperty('expand') ? {
      hotkey: "E",
      img: icons.expand.flag ? "shrink" : "expand",
      onclick: () => {
        icons.expand.flag = !icons.expand.flag;
        iconBtns.expand.img = icons.expand.flag ? "shrink" : "expand";
      },
      dataViewIcons: mapName === "dataStaMap" ? ["criteria", "expand"] : false,
    } : false;
  },

};
const criteriaPopup: typeof criteria = {
  get dataVal() {
    if (!criteria.hasOwnProperty('dataVal')) return false;
    return {
      getDays: (date: string) => {
        let days = Math.floor(new Date(date).getTime() / 86400000);
        // console.debug(date, days)
        // console.debug('criteria date=', criteria.dataVal['date'])
        return days;
      },
      oninput: ({
        minValue,
        maxValue,
      }, key: string) => {
        // console.debug(e)
        let
          max = maxValue,
          min = minValue;

        switch (key) {
          case 'az':
            if (max - min > 360)
              max = min + 360;
            if (max < 0) max = 0;
            break;
          case 'date':
            let getISOString = (days: number) => {
              let date = new Date(days * 86400000).toISOString();
              return date.split('T')[0];
            };
            [min, max] = [min, max].map(days => getISOString(days));
            break;
        }

        Object.assign(criteria.dataVal[key].current, [min, max]);

      },
    };
  },
  get station() {
    if (!criteria.hasOwnProperty('station')) return false;
    return {
      selectAll: (e: Event) => {
        let keys = Object.keys(criteria.station.showList);

        //==全部都勾就全部取消
        if (keys.every(key => criteria.station.checkList[key]))
          keys.forEach(key => criteria.station.checkList[key] = false);
        else
          keys.forEach(key => criteria.station.checkList[key] = true);
      },
      turnPage: (e: Event, next: boolean) => {
        if (next && (criteria.station.page.currPage < criteria.station.page.totalPage))
          criteria.station.page.currPage++;
        else if (!next && criteria.station.page.currPage > 1)
          criteria.station.page.currPage--;

        // console.debug(criteria.station.page.currPage, criteria.station.page.totalPage);
      },
    };
  },
  get location() {
    return criteria.hasOwnProperty('location') ? {
      oninput: (e: {
        max: number
        maxValue: number
        min: number
        minValue: number
      }) => {
        // console.debug(e)
      },
    } : false;
  },
};
const displayPopup: typeof display = {
  // get legend() {
  //   return legend ? {
  //   } : false;
  // },
  get audio() {
    let audio = display.audio;
    return audio ? {
      get volume() {
        return audio.hasOwnProperty('volume') ? {
          hotkey: "A",
          onclick: () => audio.volume[0] = !audio.volume[0],
          oninput: (e: PointerEvent) => audio.volume[1] = (e.target as HTMLSelectElement).value,
        } : false;
      },
      get alertThreshold() {
        return audio.hasOwnProperty('alertThreshold') ? {
          oninput1: (e: PointerEvent) => audio.alertThreshold[0] = (e.target as HTMLSelectElement).value,
          oninput2: (e: PointerEvent) => audio.alertThreshold[1] = (e.target as HTMLSelectElement).value,
        } : false;
      },
      get soundEffect() {
        return audio.hasOwnProperty('soundEffect') ? {
          options: {
            "piano": 0,
            "calling": 1,
            "fairies2": 2,
            "siren1": 3,
            "machine_call": 4,
            "strange_bell": 5,
            "attack_bell": 6,
          },
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            audio.soundEffect = selectVal;
          },
        } : false;
      },
    } : false;
  },
  get marker() {
    let marker = display.marker;
    return marker ? {
      get markerData() {
        return marker.hasOwnProperty('markerData') ? {
          options: Object.keys(criteria.dataVal),
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            marker.markerData = selectVal;
          }
        } : false;
      },
      get markerSize() {
        return marker.hasOwnProperty('markerSize');
      },
      get markerColor() {
        return marker.hasOwnProperty('markerColor') ? {
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            marker.markerColor = selectVal;
          }
        } : false;
      },
      get markerCluster() {
        return marker.hasOwnProperty('markerCluster') ? {
          onchange: () => marker.markerCluster = !marker.markerCluster
        } : false;
      },
      get markerShape() {
        return marker.hasOwnProperty('markerShape') ? {
          options: {
            "triangle": 0,
            "circle": 1,
          },
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            marker.markerShape = selectVal;
          },
        } : false;
      },
      get markerOpacity() {
        return marker.hasOwnProperty('markerOpacity') ? {
          oninput: (e: PointerEvent) => marker.markerOpacity = (e.target as HTMLSelectElement).value,
        } : false;
      },
    } : false;
  },
  get anime() {
    let anime = display.anime;
    return anime ? {
      get animeStyle() {
        return anime.hasOwnProperty('animeStyle') ? {
          options: {
            "none": 0,
            "living": 1,
            "pulsate": 2,
          },
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            anime.animeStyle = selectVal;
          }
        } : false;
      },
      get animeColor() {
        return anime.hasOwnProperty('animeColor') ? {
          onchange: (e: Event) => {
            let selectVal = (e.target as HTMLSelectElement).value;
            anime.animeColor = selectVal;
          }
        } : false;
      },
    } : false;
  },
  get legend() {
    return legend ? {
      get Legend() {
        return legend.hasOwnProperty('Legend') ? {
          onchange: () => legend.Legend = !legend.Legend,
        } : false
      },
      get gridLine() {
        return legend.hasOwnProperty('gridLine') ? {
          onchange: () => legend.gridLine = !legend.gridLine,
        } : false
      },
    } : false;
  },
  get overlay() {
    let overlay = display.overlay;
    return overlay && overlay.image[2] !== 'logo' ? {
      get image() {
        return overlay.hasOwnProperty('image') ? {
          onclick: () => overlay.image[0] = !overlay.image[0],
          oninput: (e: PointerEvent) => overlay.image[1] = (e.target as HTMLSelectElement).value,
        } : false
      },
    } : false;

  },
};
const graphicsPopup: typeof display = {
  onclick: (e: PointerEvent) => {
    graphics.showType = (e.target as HTMLButtonElement).value;
    graphics.trigger = !graphics.trigger;
  },

};


//===bind hotkeys
const useKeyboardBindings = (map: { [key: string]: any }) => {
  // console.debug(map)
  const handlePress = (e: KeyboardEvent) => {
    let key = e.key.length === 1 ? e.key.toUpperCase() : e.key;
    const handler = map[key];
    // console.debug(e.key, key)
    if (typeof handler === "function") {
      handler();
    }
  };
  onMounted(() => {
    window.addEventListener("keydown", handlePress);
  });
  onUnmounted(() => {
    window.removeEventListener("keydown", handlePress);
  });
};
const getBindMap = () => {
  let needHotkeys: { [key: string]: any } = {};
  if (icons)
    Object.keys(icons).forEach(key => {
      let btn = iconBtns[key];
      needHotkeys[btn.hotkey] = btn.onclick;
    });
  if (display?.audio) {
    let volume = displayPopup.audio.volume;
    needHotkeys[volume.hotkey] = volume.onclick;
  };
  return needHotkeys;
};
useKeyboardBindings(getBindMap());


onMounted(() => {
  //==legend Draggable
  //todo: 拖曳會LAG
  let legendNodes: NodeListOf<HTMLDivElement> = document.querySelectorAll(".legend>div")
  // console.debug(legendNodes);

  legendNodes
    .forEach((legend, i) => {
      new L.Draggable(legend).enable();
    });

  //==透過d3 function產生的Legend
  if (legend?.hasOwnProperty('Legend')) {
    let domainDataReady = new Promise(resolve => {
      let unWatch = watch(() => criteria.dataVal, (data, od) => {
        // console.debug(data)
        if (Object.keys(data).length) {
          unWatch();
          resolve(true);
        }
      }, { deep: true });
    });
    // console.debug(domainDataReady)
  };
});
</script>

<template>
  <div class="controller" v-if="icons">
    <div :class="`toolbar d-flex flex-column ${props.theme}`">
      <!-- icons -->
      <div v-for="(value, key) in icons" :key="value" class="icons">
        <!-- iconButton -->
        <div class="toolButton" v-show="iconBtns.expand?.dataViewIcons ?
    (icons.expand.flag ? true : iconBtns.expand.dataViewIcons.includes(key)) : true">
          <!-- tooltip -->
          <span class="tooltipText tooltip-top">
            {{ $t(iconBtns[key].img) }} ( {{ iconBtns[key].hotkey }} )
          </span>
          <img :class="`button ${key !== 'play' && key !== 'lockView' && icons[key].flag ? 'buttonFocus' : ''
    }`" :id="`${key}Btn`" :src="getImage(`icons/${iconBtns[key].img}_${props.theme}.png`)"
            @click="iconBtns[key].onclick" />
        </div>
        <!-- popup -->
        <!------------------------- criteria --------------------------->
        <div v-if="key === 'criteria'" class="popup" v-show="icons.criteria.flag">
          <h2 class="m-0">{{ $t("criteria") }}</h2>
          <a class="close" @click="iconBtns['criteria'].onclick">×</a>
          <div class="mx-1">
            <div class="d-flex flex-column">
              <!-- dataVal filter -->
              <div v-for="(val, key) in criteria.dataVal" :key="key" class="d-flex flex-column mb-2">
                <template v-if="criteria.dataVal[key].niceRange">
                  <label class="col-form-label text-nowrap text-start fs-5 fw-bold">
                    {{ $t(`${String(key)}Filter`) +
    (String(key) === 'date' && mapName === 'eventsMap_search' ? $t('dateFilterMin', {
      date: ''
    }) : '') }} </label>
                  <!-- 拉條（日期要換算） -->
                  <MultiRangeSlider v-if="String(key) === 'date'" baseClassName="multi-range-slider-bar-only"
                    :min="criteriaPopup.dataVal.getDays(criteria.dataVal['date'].niceRange[0])"
                    :max="criteriaPopup.dataVal.getDays(criteria.dataVal['date'].niceRange[1])"
                    :minValue="criteriaPopup.dataVal.getDays(criteria.dataVal['date'].current[0])"
                    :maxValue="criteriaPopup.dataVal.getDays(criteria.dataVal['date'].current[1])" :step="1"
                    @input="criteriaPopup.dataVal.oninput($event, key)" />
                  <MultiRangeSlider v-else baseClassName="multi-range-slider-bar-only"
                    :min="criteria.dataVal[key].niceRange[0]" :max="criteria.dataVal[key].niceRange[1]" :step="1"
                    :minValue="criteria.dataVal[key].current[0]" :maxValue="criteria.dataVal[key].current[1]"
                    @input="criteriaPopup.dataVal.oninput($event, key)" />
                  <!-- 輸入框 -->
                  <div class="d-flex flex-row flex-nowrap">
                    <input class="form-control" :type="String(key) === 'date' ? 'date' : 'number'"
                      :min="criteria.dataVal[key].niceRange[0]" :max="criteria.dataVal[key].niceRange[1]" :step="1"
                      v-model.lazy="criteria.dataVal[key].current[0]" />
                    <span class="p-1">-</span>
                    <input class="form-control" :type="String(key) === 'date' ? 'date' : 'number'"
                      :min="criteria.dataVal[key].niceRange[0]" :max="criteria.dataVal[key].niceRange[1]" :step="1"
                      v-model.lazy="criteria.dataVal[key].current[1]" />
                  </div>
                </template>
              </div>
              <!-- station filter -->
              <div v-if="criteria.station" class="d-flex flex-column mb-2 ">
                <label class="col-form-label text-nowrap text-start fs-5 fw-bold">{{ $t("stationFilter") }}
                </label>
                <div class="btn-group dropend">
                  <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown"
                    aria-expanded="false" data-bs-auto-close="outside">{{
    $t("select") }}</button>
                  <ul class="dropdown-menu p-3" v-for="page in [criteria.station.page]">
                    <template v-if="page.totalPage">
                      <!-- un/selectAll -->
                      <button type="button" class="btn btn-secondary mb-1" @click="criteriaPopup.station.selectAll">
                        {{ $t(`${Object.keys(criteria.station.showList).every(key => criteria.station.checkList[key]) ?
    'unselectAll' : 'selectAll'}`) }}
                      </button>
                      <hr>
                      <!-- station checkboxes -->
                      <div class="d-flex flex-row flex-wrap">
                        <div v-for="(sta, idx) in 
                      Object.keys(criteria.station.showList).sort((a, b) => a > b ? 1 : -1)" :key="sta"
                          v-show="(idx >= 10 * (page.currPage - 1)) && (idx < 10 * page.currPage)"
                          class="form-check col-6 text-start">
                          <input class="form-check-input" type="checkbox" :id="`${sta}_ckb`"
                            v-model="criteria.station.checkList[sta]" />
                          <label class="form-check-label text-nowrap" :for="`${sta}_ckb`">
                            {{ (sta.toString()) }}
                          </label>
                        </div>
                      </div>
                      <!-- page controller -->
                      <div class="d-flex flex-row justify-content-center">
                        <label class="text-center">{{ $t("stationPage") }}</label>
                      </div>
                      <div class="d-flex flex-row flex-nowrap justify-content-around">
                        <button type="button" class="col-2 btn btn-outline-secondary btn-sm"
                          @click="criteriaPopup.station.turnPage($event, false)">&lt;</button>
                        <div class="col-6 d-flex flex-row flex-nowrap align-items-center">
                          <input class="form-control" type="text" v-model="criteria.station.page.currPage">
                          <label class="col-form-label col-4">
                            {{ `/ ${page.totalPage}` }}
                          </label>
                        </div>
                        <button type="button" class="col-2 btn btn-outline-secondary btn-sm"
                          @click="criteriaPopup.station.turnPage($event, true)">&gt;</button>
                      </div>
                    </template>

                  </ul>
                </div>
              </div>
              <!-- location filter -->
              <div v-if="criteriaPopup.location" class="d-flex flex-column mb-2">
                <label class="text-start fs-5 fw-bold col-2">{{
    $t("locationFilter")
  }}</label>
                <table>
                  <tbody>
                    <tr>
                      <td>
                        <div class="d-flex flex-row align-items-center">
                          <label style="font-size: 0.5em">W</label>
                          <input type="text" size="8" class="form-control ms-1"
                            v-model.lazy.number="criteria.location.lon[0]" />
                        </div>
                      </td>
                      <td>
                        <label style="font-size: 0.5em">N</label>
                        <input type="text" size="8" class="form-control"
                          v-model.lazy.number="criteria.location.lat[1]" />
                        <input type="text" size="8" class="form-control"
                          v-model.lazy.number="criteria.location.lat[0]" />
                        <label style="font-size: 0.5em">S</label>
                      </td>
                      <td>
                        <div class="d-flex flex-row align-items-center">
                          <input type="text" size="8" class="form-control me-1"
                            v-model.lazy.number="criteria.location.lon[1]" />
                          <label style="font-size: 0.5em">E</label>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <!------------------------- display --------------------------->
        <div v-if="key === 'display'" class="popup" v-show="icons.display.flag">
          <h2 class="m-0">{{ $t("display") }}</h2>
          <a class="close" @click="iconBtns['display'].onclick">×</a>
          <div class="mx-1">
            <!-- audio -->
            <div class="d-flex flex-column mb-3" v-if="displayPopup.audio">
              <label class="col-form-label text-nowrap text-start fs-5 fw-bold">
                {{ $t("alertDisplay") }}</label>
              <!-- volume -->
              <div class="d-flex flex-row flex-nowrap" v-if="displayPopup.audio['volume']">
                <label for="overlaySwitch" class="text-nowrap me-3">{{
    $t("switchDisplay")
  }}</label>
                <div class="ps-5 form-switch">
                  <span class="tooltipText tooltip-top">{{ $t(display.audio["volume"][0] ? "off" : "on") }} (
                    {{ displayPopup.audio["volume"].hotkey }} )</span>
                  <input class="my-1 form-check-input" type="checkbox" role="switch"
                    @click="displayPopup.audio['volume'].onclick" :checked="display.audio['volume'][0]" />
                </div>

                <!-- <input class="slider col-7 p-0" type="range" min="0" max="100" :value="display.audio['volume'][1]"
                  step="1" list="audioTick" :disabled="!display.audio['volume'][0]"
                  @input="displayPopup.audio['volume'].oninput" />
                <span class="col-2 text-nowrap" style="font-size: small">
                  <b class="fs-6">{{ display.audio['volume'][1] }}</b> %
                </span>

                <datalist class="fs-6 ps-5" id="audioTick">
                  <option v-for="val in Array.from(Array(21), (d, i) => i * 5)" :key="val" :value="val"
                    :label="val % 25 ? '' : val.toString()" v-bind:style="{
                      fontSize: 'smaller',
                      get paddingLeft() { return !(val % 25) && val ? '5px' : undefined }
                    }"></option>
                </datalist> -->
              </div>
              <!-- soundEffect -->
              <div class="soundEffect" v-if="displayPopup.audio['soundEffect']">
                <div class="d-flex flex-row flex-nowrap mb-2">
                  <label for="soundEffect" class="col-form-label text-nowrap me-3">{{
    $t("soundEffect")
  }}</label>
                  <select class="form-select" id="soundEffect" @change="displayPopup.audio['soundEffect'].onchange">
                    <option v-for="( val, opt ) in  displayPopup.audio['soundEffect'].options " :key="val" :value="val"
                      :selected="display.audio['soundEffect'] === val">
                      {{ $t(opt.toString()) }}
                    </option>
                  </select>
                </div>
              </div>
              <!-- alertThreshold -->
              <div class="alertThreshold" v-if="displayPopup.audio['alertThreshold']">
                <div class="d-flex flex-row flex-nowrap">
                  <span class="text-nowrap text-start fs-6">{{
    $t("alertThreshold1")
  }}</span>
                  <input type="number" class="form-control mx-1" placeholder="sta"
                    v-model="display.audio['alertThreshold'][0]" />
                  <span class="text-nowrap text-start fs-6">{{
    $t("alertThreshold2")
  }}</span>
                </div>
                <div class="d-flex flex-row flex-nowrap pt-1">
                  <span class="text-nowrap text-start fs-6">{{
      $t("alertThreshold3")
    }}</span>
                  <input type="number" step="0.1" class="form-control mx-1" placeholder="pga"
                    v-model="display.audio['alertThreshold'][1]" />
                  <span class="text-nowrap text-start fs-6">gal</span>
                </div>
              </div>
            </div>

            <!-- marker -->
            <div class="d-flex flex-column mb-2" v-if="displayPopup.marker">
              <label class="col-form-label text-nowrap text-start fs-5 fw-bold">{{
    $t("markerDisplay")
  }}</label>
              <!-- markerData -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerData']">
                <label for="markerData" class="col-form-label text-nowrap me-3">{{
    $t("markerData")
  }}</label>
                <select class="form-select" id="markerData" @change="displayPopup.marker['markerData'].onchange">
                  <option v-for="( opt, idx ) in  displayPopup.marker['markerData'].options " :key="opt" :value="opt"
                    :selected="display.marker['markerData'] === opt">
                    {{ $t(opt.toString()) }}
                  </option>
                </select>
              </div>
              <!-- markerSize -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerSize']">
                <label for="markerSize" class="col-form-label text-nowrap me-3">{{
    $t("markerSize")
  }}</label>
                <input type="number" class="form-control" id="markerSize" min="1" step="1"
                  v-model="display.marker['markerSize']" />
              </div>
              <!-- markerColor -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerColor']">
                <label for="markerColor" class="col-form-label text-nowrap me-3">{{
    $t("markerColor")
  }}</label>
                <input type="color" class="form-control h-auto" id="markerColor" :value="display.marker['markerColor']"
                  @change="displayPopup.marker['markerColor'].onchange" />
              </div>
              <!-- markerOpacity -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerOpacity']">
                <label for="markerOpacity" class="col-form-label text-nowrap me-3">
                  {{ $t("markerOpacity") }}
                </label>
                <div class="d-flex flex-column me-1">
                  <input class="slider" id="markerOpacity" type="range" min="0" max="1" step="0.1" list="opacityTick"
                    v-model.number.lazy="display.marker['markerOpacity']" />
                  <datalist class="fs-6" id="opacityTick">
                    <option v-for=" val  in  Array.from(Array(11), (d, i) => i) " :key="val" :value="val / 10"
                      :label="val % 5 ? '' : `${(val / 10).toString()}`" v-bind:style="{
    fontSize: 'smaller',
    get paddingLeft() {
      return !(val % 5) && val ? '27px' : undefined;
    },
  }
    "></option>
                  </datalist>
                </div>
              </div>

              <!-- markerCluster -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerCluster']">
                <label for="markerCluster" class="text-nowrap me-3">{{
    $t("markerCluster")
  }}</label>
                <div class="ps-5 form-switch">
                  <span class="tooltipText tooltip-top">{{
      $t(display.marker["markerCluster"] ? "off" : "on")
    }}</span>
                  <input class="my-1 form-check-input" type="checkbox" role="switch"
                    v-model.lazy="display.marker['markerCluster']" />
                </div>
              </div>
              <!-- markerShape -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.marker['markerShape']">
                <label for="markerShape" class="col-form-label text-nowrap me-3">{{
    $t("markerShape")
  }}</label>
                <select class="form-select" id="markerShape" @change="displayPopup.marker['markerShape'].onchange">
                  <option v-for="( val, opt ) in  displayPopup.marker['markerShape'].options " :key="val" :value="val"
                    :selected="display.marker['markerShape'] === val">
                    {{ $t(opt.toString()) }}
                  </option>
                </select>
              </div>
            </div>
            <!-- anime -->
            <div class="d-flex flex-column mb-2" v-if="displayPopup.anime && !+display.marker['markerShape']">
              <label class="col-form-label text-nowrap text-start fs-5 fw-bold">{{
    $t("animeDisplay")
  }}</label>
              <!-- animeStyle -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.anime['animeStyle']">
                <label for="animeStyle" class="col-form-label text-nowrap me-3">{{
    $t("animeStyle")
  }}</label>
                <select class="form-select" id="animeStyle" @change="displayPopup.anime['animeStyle'].onchange">
                  <option v-for="( val, opt ) in  displayPopup.anime['animeStyle'].options " :key="val" :value="val"
                    :selected="display.anime['animeStyle'] === val">
                    {{ $t(opt.toString()) }}
                  </option>
                </select>
              </div>
              <!-- animeColor -->
              <div class="d-flex flex-row flex-nowrap mb-2" v-if="displayPopup.anime['animeColor']">
                <label for="animeColor" class="col-form-label text-nowrap me-3">{{
    $t("animeColor")
  }}</label>
                <input type="color" class="form-control h-auto" id="animeColor" :value="display.anime['animeColor']"
                  @input="displayPopup.anime['animeColor'].onchange" />
              </div>
            </div>

            <!-- overlay -->
            <div class="d-flex flex-column mb-2" v-if="displayPopup.overlay">
              <label class="col-form-label text-nowrap text-start fs-5 fw-bold">{{
    $t("overlayDisplay")
  }}</label>
              <!--overlay switch -->
              <div class="d-flex flex-row flex-nowrap" v-if="displayPopup.overlay['image']">
                <label for="overlaySwitch" class="text-nowrap me-3">{{
    $t("switchDisplay")
  }}</label>
                <div class="ps-5 form-switch">
                  <span class="tooltipText tooltip-top">{{
      $t(display.overlay["image"][0] ? "off" : "on")
    }}</span>
                  <input class="my-1 form-check-input" id="overlaySwitch" type="checkbox" role="switch"
                    v-model.lazy="display.overlay['image'][0]" />
                </div>
              </div>
              <!--overlay opacity -->
              <div class="d-flex flex-row flex-nowrap" v-if="displayPopup.overlay['image']">
                <label for="overlayOpacity" class="col-form-label text-nowrap me-3">{{
    $t("overlayOpacity")
  }}</label>
                <div class="d-flex flex-column me-1">
                  <input class="slider" id="overlayOpacity" type="range" min="0" max="1" step="0.1" list="opacityTick"
                    v-model.number.lazy="display.overlay['image'][1]" />
                  <datalist class="fs-6" id="opacityTick">
                    <option v-for=" val  in  Array.from(Array(11), (d, i) => i)" :key="val" :value="val / 10"
                      :label="val % 5 ? '' : `${(val / 10).toString()}`" v-bind:style="{
    fontSize: 'smaller',
    get paddingLeft() {
      return !(val % 5) && val ? '27px' : undefined;
    },
  }
    ">
                    </option>
                  </datalist>
                </div>
              </div>
            </div>

            <!-- show checkbox -->
            <div v-if="legend" class="row mb-2">
              <div v-for="(val, key) in legend" :key="val" class="form-check col-12 text-start">
                <input class="form-check-input" type="checkbox" :id="`${key}_ckb`"
                  @change="displayPopup.legend[key].onchange" :checked="val" />
                <label class="form-check-label text-nowrap" :for="`${key}_ckb`">
                  {{ $t(key.toString()) }}</label>
              </div>
              <!-- <div v-if="gridLine" class="form-check col-6 text-start">
                <input class="form-check-input" type="checkbox" id="gridLine_ckb" checked />
                <label class="form-check-label" for="gridLine_ckb">gridLine</label>
              </div> -->
            </div>
          </div>
        </div>
        <!------------------------- graphics --------------------------->
        <div v-if="key === 'graphics'" class="popup" v-show="icons.graphics.flag">
          <h2 class="m-0">{{ $t("graphics") }}</h2>
          <a class="close" @click="iconBtns['graphics'].onclick">×</a>
          <div class="mx-1">

            <div v-for="(graphs, type) in graphics.type" :key="type">
              <div v-if="graphs">
                <label class="col-form-label text-nowrap text-start fs-6 fw-bold d-block">
                  {{ $t(type.toString()) }}</label>
                <div
                  :class="type.toString() === 'animeGraphics' ? 'd-flex flex-row mb-2 justify-content-around' : 'd-flex flex-column mb-2'">
                  <button v-for="graph in graphs" :key="graph" type="button"
                    class="text-nowrap btn btn-secondary my-1 mx-3" @click="graphicsPopup.onclick" :value="graph">
                    {{ $t(graph) }}
                  </button>
                </div>
              </div>
            </div>


          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="legend" v-if="legend">
    <div class="Legend" v-if="displayPopup.legend['Legend']" v-show="legend['Legend']">
    </div>
  </div>
</template>

<style scoped>
/* =============================================toolbar========================================== */
.controller {
  position: absolute;
  bottom: 5%;
  z-index: 1600;
  pointer-events: auto;
}

.toolbar.white {
  margin: 10px 10px;
  background: rgba(255, 255, 255, 0.2);
  padding: 3px 5px 0 5px;
  border: 2px solid #fff;
  border-radius: 50px;
  background-clip: padding-box;
  text-align: center;
}

.toolbar.black {
  margin: 10px 10px;
  background: rgba(0, 0, 0, 0.1);
  padding: 3px 5px 0 5px;
  border: 2px solid #000;
  border-radius: 50px;
  background-clip: padding-box;
  text-align: center;
}

.icons {
  position: relative;
}

.toolButton {
  position: relative;
  padding: 6px 0px;
}

.toolButton:hover .tooltipText {
  visibility: visible;
}

.button {
  padding: 5px;
  cursor: pointer;
  width: 50px;
  height: 50px;
  border-radius: 10px;
  transition: all 0.2s ease-out;
}

.button:hover {
  background: #06d85f;
}

.buttonFocus {
  animation: iconBlink 1s linear infinite;
}

@keyframes iconBlink {
  0% {
    background: false;
  }

  50% {
    background: #06d85f;
  }

  100% {
    background: false;
  }
}

.toolbar .tooltipText {
  visibility: hidden;
  position: absolute;
  background-color: #555;
  color: #fff;
  font-size: 18px;
  text-align: center;
  padding: 5px 10px;
  border-radius: 6px;
  white-space: nowrap;
  /* opacity: 0; */
  /* transition: opacity .6s; */
  transform: translateX(-50%);
  z-index: 100;
  pointer-events: none;
}

.tooltip-top {
  bottom: 105%;
  left: 50%;
}

.tooltip-top::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}

/*============================================ pannel ============================================*/

.popup {
  margin: auto 70px;
  padding: 5px 20px;
  border-radius: 5px;
  min-width: 260px;
  max-width: 330px;
  position: absolute;
  bottom: 20%;
  animation: popupShow 0.2s;
}

.popup:after {
  content: "";
  position: absolute;
  bottom: 12px;
  left: -20px;
  border-style: solid;
  border-width: 10px;
}

.toolbar.white .popup {
  background: #fff;
}

.toolbar.white .popup:after {
  border-color: transparent white white transparent;
}

.toolbar.black .popup {
  background: rgb(230, 224, 224);
}

.toolbar.black .popup:after {
  border-color: transparent rgb(230, 224, 224) rgb(230, 224, 224) transparent;
}

.popup h2 {
  margin-top: 0;
  color: #333;
  font-family: Tahoma, Arial, sans-serif;
  white-space: nowrap;
}

.popup .close {
  position: absolute;
  top: 20px;
  right: 30px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}

.popup .close:hover {
  color: #06d85f;
}

.popup .content {
  max-height: 30%;
  overflow: auto;
}

.popup label {
  white-space: nowrap;
}

/* @media screen and (max-width: 700px) {
    .toolbar {
        width: 70%;
    }
    .popup {
        width: 70%;
    }
} */

@keyframes popupShow {
  0% {
    transform: scale(0.1);
  }

  100% {
    transform: scale(1);
  }
}

.dropdown-menu input,
.dropdown-menu select {
  /* min-width: 5em; */
  max-width: 10em;
}

datalist {
  display: inline-flex;
}

.alertThreshold input[type="number"] {
  width: 40px;
  border: 0;
  outline: 0;
  background: transparent;
  border-bottom: 1px solid black;
  padding: 0;
  border-radius: 0;
  text-align: center;
}

.alertThreshold {
  /* margin-left: em; */
}

/* Chrome, Safari, Edge, Opera */
.alertThreshold input::-webkit-outer-spin-button,
.alertThreshold input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
.alertThreshold input[type="number"] {
  -moz-appearance: textfield;
}

/*============================================ bootstrap-slider ============================================ */
:deep(.multi-range-slider-bar-only) {
  padding-top: 0;
}

:deep(.multi-range-slider-bar-only) .caption {
  display: none !important;
}

:deep(.multi-range-slider-bar-only) .thumb::before {
  --slider-handle-width: 16px;
  width: var(--slider-handle-width);
  height: var(--slider-handle-width);
  margin-top: -3px;
  background-color: #0480be;
  border: unset;
  box-shadow: unset;
}

:deep(.multi-range-slider-bar-only) .bar-inner {
  background-color: #0480be;
  border: unset;
  box-shadow: unset;
}

:deep(.multi-range-slider-bar-only) .bar-left,
:deep(.multi-range-slider-bar-only) .bar-right {
  border-color: #afafafb9;
  border-style: solid;
  border-width: 1px;
  box-shadow: inset 0 1px 2px rgb(0 0 0 / 10%);
  background-color: #f7f7f7;
}

/* =========legend========= */
.legend {
  position: absolute;
  z-index: 1500;
  bottom: 15%;
  right: 5%;
  pointer-events: none;
}

.legend>* {
  cursor: grab;
  pointer-events: all;
  position: absolute;
  z-index: 0;
  top: 0;
  right: 0;
}

.legend :deep(text) {
  font: bold 16px sans-serif;
  fill: black;
  paint-order: stroke;
  stroke-width: 2px;
  stroke: white;
  stroke-linecap: butt;
  stroke-linejoin: miter;
}

.Legend :deep(svg>image),
.Legend :deep(svg>g:first-child) {
  outline: solid 2px black;
}
</style>
