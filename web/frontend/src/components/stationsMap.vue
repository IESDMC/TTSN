<script setup lang="ts">
import { updateHandler } from '@/components/statics/functions.js';
import type { dataType, mapControllerType, staInfoType, UIControlsType } from "@/components/statics/types";
import mapUI from "@/components/UI/mapUI.vue";
import { useDataListStore } from "@/stores/getDataList";
import { useStaListStore } from "@/stores/getStaList";
import { LCircleMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import * as d3 from "d3";
import { computed, onMounted, reactive, ref, watch, type PropType } from "vue";
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n({ inheritLocale: true });
const staListStore = useStaListStore();
const staList = computed(() => staListStore.staList);
const userStaList = ref();//==使用者挑的測站列表
const markers = ref();

const emits = defineEmits(['changeDataList', 'getMapController']);
const props = defineProps({
    isDataView: {
        type: Boolean,
        default: null,
        required: false,
    },
    UIControls: {
        type: Object as PropType<UIControlsType<staInfoType | dataType>>,
        required: true,
    },
});

const isDataView = props.isDataView;
const tableTarget = props.UIControls.tableTarget;
const dialogControls = props.UIControls.dialogUI;
const others = props.UIControls.others;

const mapController: mapControllerType = {
    icons:
        reactive({
            criteria: {
                flag: isDataView,
                popup: isDataView ?
                    {
                        dataVal: { date: [], },
                        station: { checkList: {}, showList: {}, page: {} }
                    } :
                    { location: { lat: [], lon: [], } }
            },
            display: {
                flag: false,
                popup: {
                    marker: {
                        markerSize: 5,
                        markerColor: '#FF0000',
                        markerOpacity: 0.3,
                    },
                    legend: {
                        Legend: true,
                        gridLine: true,
                    },
                }
            },
            lockView: {
                flag: false,
                popup: {
                }
            },
            expand: {
                flag: others.mapExpand,
                popup: {
                }
            },
        }),
    mapEvent: reactive({
        bounds: undefined,
        mapShift: 0,
        mapObj: null,
    }),
    mapName: isDataView ? 'dataStaMap' : 'stationsMap'
};
let icons = mapController.icons,
    mapEvent = mapController.mapEvent;
let criteria = icons.criteria.popup,
    display = icons.display.popup;


onMounted(() => {
    const getIsInRangeFun = (range: number[]) => {
        let fun: (arg0: number) => boolean;
        fun = (x: number) =>
            (!isNaN(range[0]) ? x >= range[0] : true) && (!isNaN(range[1]) ? x <= range[1] : true)
        return fun;
    };
    //==filters
    const updateObj = {
        updateFlag: true,
        updateTimeOut: null,
        updateDelay: 50,
    };

    staListStore.getStaList();

    if (isDataView) {
        const initFilter = () => {
            if (criteria.station) {
                const rowsPerPage = 10;

                let list = staList.value.map(d => d.station);
                let filterObj = list.reduce(
                    (obj, cur) => ({ ...obj, [cur]: true }), {});
                Object.assign(criteria.station.checkList, { ...filterObj });
                Object.assign(criteria.station.showList, { ...filterObj });
                Object.assign(criteria.station.page, {
                    rowsPerPage,
                    currPage: 1,
                    totalPage: Math.ceil(list.length / rowsPerPage),
                });

                // console.debug(criteria.station);
            };
            if (criteria.dataVal) {
                const dataValeKeys = Object.keys(criteria.dataVal);//{date}
                const niceMultiplier = {
                    // ml: 1,
                    // depth: 5,
                };

                //==根據資料值來算可選範圍
                let valExtArr = dataValeKeys.map(key => {
                    return d3.extent(dataList.value.map((d) => d[key]).filter(v => !isNaN(parseInt(v))));
                });
                let dataValObj = dataValeKeys.reduce((obj, key, i) => {
                    let rawRange = valExtArr[i],
                        multi = niceMultiplier[key] ?? 1;

                    let niceRange = key === 'date' ?
                        rawRange.map(val => val) :
                        rawRange.map((val, i) => Math[i ? 'ceil' : 'floor'](val / multi) * multi);

                    return {
                        ...obj,
                        [key]: {
                            current: [...niceRange],
                            niceRange,
                            rawRange
                        }
                    }
                }, {});
                Object.assign(criteria.dataVal, dataValObj);
            }
            // console.debug(criteria.dataVal.date);
        };

        const dataListStore = useDataListStore();
        dataListStore.getDataList();
        const dataList = computed(() => dataListStore.dataList);
        const userDataList = ref();//==使用者挑的資料列表

        //==取得資料後初始篩選陣列一次
        let unwatch_init = watch([dataList, staList], (listArr) => {
            let dataList = listArr[0],
                staList = listArr[1];
            // console.debug(staList, dataList);
            if (dataList && staList) {
                userStaList.value = staList;
                userDataList.value = dataList;
                others.tableAllStaTotal = dataList.length;
                initFilter();
                unwatch_init();
            }
        }, { deep: true });

        emits("getMapController", mapController);

        //==設定要監聽的屬性，避免不用來篩選的屬性觸發
        const criteriaFilters = [criteria.dataVal, criteria.station.checkList,];
        watch(criteriaFilters, (filterArr) => {
            if (!userDataList.value) return;

            let action = () => {
                let filter = {
                    dataVal: filterArr[0],
                    staList: filterArr[1],
                };
                const dataValKeys = Object.keys(filter.dataVal);

                let dataFilters = dataValKeys.map(key =>
                    getIsInRangeFun(key === 'date' ?
                        filter.dataVal.date.current.map(d => new Date(d).getTime()) :
                        filter.dataVal[key].current)
                );
                let stationFilter = (key: string) => filter.staList[key];

                //==先篩date來得到data列表
                let tmpData = dataList.value.filter((d) => dataFilters.every((fun, i) =>
                    fun(dataValKeys[i] === 'date' ?
                        new Date(d.date).getTime() :
                        d[dataValKeys[i]]))
                );
                userDataList.value = tmpData.filter((d: dataType) =>
                    stationFilter(d.station)
                );

                let newStaList = [... new Set(tmpData.map(d => d.station))] as string[];
                userStaList.value = staList.value.filter(d => newStaList.includes(d.station));
                // console.debug(newStaList);

                //==根據選擇的paper來決定station篩選要顯示的checkBox
                let showList = newStaList.reduce((obj, cur) => ({ ...obj, [cur]: true }), {});
                let totalPage = Math.ceil(newStaList.length / criteria.station.page.rowsPerPage)

                criteria.station.showList = showList;
                Object.assign(criteria.station.page, {
                    currPage: criteria.station.page.totalPage === totalPage ?
                        criteria.station.page.currPage : 1,
                    totalPage
                });
            };
            updateHandler(action, updateObj);
            // tableTarget.selectFlag = false;
        }, { deep: true });

        //==更新dataTable
        watch(userDataList, (list) => {
            emits("changeDataList", list);
        });
    }
    else {
        //==取得資料後初始篩選陣列一次
        let unwatch_init = watch(staList, (list) => {
            userStaList.value = list;
            others.tableAllStaTotal = list.length;
            unwatch_init();
        }, { deep: true });


        //==設定要監聽的屬性，避免不用來篩選的屬性觸發
        const criteriaFilters = [criteria.location];
        watch(criteriaFilters, (filterArr) => {
            // console.debug(filterArr);
            let action = () => {
                let filter = {
                    location: filterArr[0],
                };
                // console.debug(filter);
                let locationKeys = ['lat', 'lon'],
                    locationFilter = locationKeys.map(key =>
                        getIsInRangeFun(filter.location[key].map(v => !isNaN(parseInt(v)) ? v : undefined)));

                userStaList.value = staList.value.filter((res) =>
                    locationFilter.every((fun, i) => fun(+res[locationKeys[i]]))
                );
            };
            updateHandler(action, updateObj);
        }, { deep: true });

        //==更新dataTable
        watch(userStaList, (list) => {
            emits("changeDataList", list);
        });

    }

    //地圖展延
    watch(() => icons.expand.flag, (flag) => {
        if (others) others.mapExpand = flag;
    }, { deep: true });

    // Table Events
    if (!tableTarget) return;
    watch(() => tableTarget.hovered, (enter, out) => {

        let hovered = enter?.row,
            leaved = out?.row;
        // console.debug(enter);

        const findMarker = (hovered: staInfoType | dataType) =>
            markers.value.find((m: { name: string }) => m.name === `${hovered.station}`)?.leafletObject;

        if (hovered) {
            let targetMarker = findMarker(hovered);
            // console.debug(targetMarker);
            if (targetMarker) {
                targetMarker.openPopup();
                targetMarker.getElement().classList.add('jumpingMarker');
            }
        }
        else if (leaved) {
            let targetMarker = findMarker(leaved)
            if (targetMarker) {
                targetMarker.closePopup();
                targetMarker.getElement().classList.remove('jumpingMarker');
            }
        }

    }, { deep: true });
    watch(() => tableTarget.clicked, (clicked) => {
        if (!isDataView || !clicked) return;
        const refClass = 'td_link';

        let target = <HTMLTableRowElement>clicked.event.target,
            data = <dataType>clicked.row;
        // console.debug(clicked, data);

        if (target.classList.contains(refClass) ||
            (target.parentNode as HTMLTableElement).classList.contains(refClass))
            Object.assign(dialogControls.content, {
                type: 'scanView',
                data: { ...data }//給新的參考讓vue watch觸發
            });


        tableTarget.clicked = undefined;

    }, { deep: true });


});

</script>

<template>
    <mapUI :mapController="mapController">
        <template #mapLayers>
            <div v-for="(staObj, index) in   userStaList  " :key="index">
                <LCircleMarker :lat-lng="[staObj.lat, staObj.lon]" :color="display.marker['markerColor']" :opacity="1"
                    :weight="1" :radius="display.marker['markerSize']" :fill="true"
                    :fillOpacity="display.marker['markerOpacity']" :fillColor="display.marker['markerColor']"
                    :name="staObj.station" ref="markers">
                    <LPopup>
                        <h3>{{ `${staObj.station} ` }}</h3>
                        {{ `${$t("stationName")} : ${staObj[locale === "en" ? 'nameEnglish' : 'nameChinese']}` }}<br />
                        {{ `${$t("latitude")} : ${staObj.lat}°` }}<br />
                        {{ `${$t("longitude")} : ${staObj.lon}°` }}<br />
                        {{ `${$t("elev")} : ${staObj.elev} m` }}<br />
                        {{ `${$t("gain")} : ${staObj.gain} ` }}<br />

                    </LPopup>
                </LCircleMarker>
            </div>
        </template>
    </mapUI>
</template>

<style lang="scss" scoped>
hr {
    margin: 0;
}


:deep(div.jumpingMarker) {
    animation: triangle-yo-yo 0.5s ease-in-out 0s infinite normal;
    z-index: 9999 !important;

    &::after {
        content: "";
        width: 100%;
        height: 100%;
        border-radius: 50%;
        position: absolute;
        left: 50%;
        top: 50%;
        z-index: -1;
        transform: translate(-50%, -50%);
        transform-origin: 50%;
        pointer-events: none;
        background-color: white;
        opacity: 0.5;
        animation: living 1s linear infinite;
    }
}

@keyframes triangle-yo-yo {
    0% {
        top: 10px;
    }

    33% {
        top: 0;
    }

    66% {
        top: -10px;
    }

    100% {
        top: 0;
    }
}

@keyframes living {

    /*圓形放大的同時，透明度逐漸減小為0*/
    0% {
        width: 0%;
        height: 0%;
    }

    50% {
        width: 800%;
        height: 800%;
    }

    100% {
        width: 0%;
        height: 0%;
    }
}

:deep(path.jumpingMarker) {
    animation: circle-yo-yo 0.5s ease-in-out 0s infinite normal;
    stroke: white;
    stroke-opacity: 0.3;
    stroke-linecap: round;
    fill-opacity: 1;
}

@keyframes circle-yo-yo {
    0% {
        transform: translate(0, 10px);
        stroke-width: 1;
    }

    33% {
        transform: translate(0, 0);
        stroke-width: 50;
    }

    66% {
        transform: translate(0, -10px);
        stroke-width: 50;
    }

    100% {
        transform: translate(0, 0);
        stroke-width: 1;
    }
}
</style>