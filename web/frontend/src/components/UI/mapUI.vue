<script setup lang="ts">
import "@/components/statics/Leaflet.Graticule.js";
import { tileProviders } from "@/components/statics/tileProviders";
import type { mapControllerType } from "@/components/statics/types";
import mapControllerUI from "@/components/UI/mapControllerUI.vue";
import MarkerCluster from "@/components/UI/MarkerCluster.vue";
import {
    LControlLayers, LMap, LTileLayer
} from "@vue-leaflet/vue-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ref, watch, type PropType } from "vue";

const props = defineProps({
    mapController: {
        type: Object as PropType<mapControllerType>,
        required: true,
    }
});
const icons = props.mapController.icons;
const display = icons.display?.popup,
    legend = display?.legend,
    mapEvent = props.mapController.mapEvent,
    mapName = props.mapController.mapName;
// console.debug('mapName=', mapName)

const map = ref<any>(null);
const mapCenter = [23.5, 120];
const mapBounds = [[-90, -180], [90, 180]];
const defaultTile = "WorldImagery";
const theme = ref('white');
const cluster = ref<any>(null);
const clusterFlag = ref(display.marker.markerCluster);

const readyHandler = () => {
    const leafletMap = map.value.leafletObject;
    mapEvent.mapObj = leafletMap;

    // leafletMap.doubleClickZoom.disable();
    // console.debug('cluster', cluster)
    const lockMap = (lock: boolean) => {
        const mapEvents = [
            "boxZoom",
            "scrollWheelZoom",
            "doubleClickZoom",
            "dragging",
            "keyboard",
        ];
        let action = lock ? "disable" : "enable";
        mapEvents.forEach((event) => leafletMap[event][action]());
    };
    watch(() => icons.lockView.flag, (flag) => {
        lockMap(flag);
    }, { immediate: true });

    if (icons.hasOwnProperty('expand')) {
        watch(() => icons.expand.flag, (flag) => {
            if (flag) leafletMap.setView(mapCenter, 7, { animate: false });

            // leafletMap.fitWorld();
            leafletMap.invalidateSize();

        }, { immediate: true });
    };
    if (display.marker.hasOwnProperty('markerCluster')) {
        watch(() => display.marker.markerCluster, (nV, oV) => {
            // console.debug(nV);
            clusterFlag.value = nV;
        }, { immediate: true });
    };
    if (legend.hasOwnProperty('gridLine')) {
        let latlngLayer: any;
        const makeGrid = (color: string) => {
            // 移除無法清除創建時註冊的事件
            // if (latlngLayer) leafletMap.removeLayer(latlngLayer);
            if (!latlngLayer)
                latlngLayer = L.latlngGraticule({
                    showLabel: true,
                    color,
                    zoomInterval: [
                        { start: 2, end: 3, interval: 30 },
                        { start: 4, end: 4, interval: 10 },
                        { start: 5, end: 6, interval: 5 },
                        { start: 7, end: 8, interval: 1.5 },
                        { start: 9, end: 9, interval: 0.5 },
                        { start: 10, end: 11, interval: 0.2 },
                        { start: 12, end: 14, interval: 0.1 },
                        { start: 15, end: 18, interval: 0.05 },
                    ],
                }).addTo(leafletMap);
            else {
                Object.assign(latlngLayer.options, {
                    color,
                    fontColor: color,
                });
                latlngLayer._reset();
            };
            // console.debug(latlngLayer)
        };
        const displayGrid = (flag: boolean) => {
            latlngLayer._canvas.style.display = flag ? "inline" : "none";
        };

        watch(() => legend.gridLine, (flag) => displayGrid(flag));

        leafletMap.on("baselayerchange", (layer: any) => {
            let color = tileProviders.find(map => map.name === layer.name).color;
            makeGrid(color);
            displayGrid(legend.gridLine);
            theme.value = color;
            // console.debug(theme.value);
        });
    };
    {
        // 監聽地圖移動結束的事件
        // leafletMap.on('moveend', function () {

        //     // 獲取當前地圖的經緯度範圍
        //     let bounds = leafletMap.getBounds();

        //     // 獲取當前地圖的縮放級別
        //     let zoom = leafletMap.getZoom();

        //     // 更新瓦片圖層的範圍和縮放級別.
        //     console.debug(layer)
        //     layer.value.forEach((l: any) => {
        //         console.debug(l)
        //         l.setBounds(bounds);
        //         l.setZoom(zoom);
        //     });
        //     // leafletMap.eachLayer(function (layer: any) {
        //     //     console.debug(layer)
        //     //     // layer.setBounds(bounds);
        //     //     // layer.setZoom(zoom);
        //     //     // console.debug(layer)
        //     // });
        //     // let aaa = leafletMap.getLayers()
        //     // console.debug(aaa)

        //     // tileLayer.setBounds(bounds);
        //     // tileLayer.setZoom(zoom);
        // });
        // let bounds = L.latLngBounds(mapBounds);
        // leafletMap.setMaxBounds(mapBounds);
        // leafletMap.wrapLatLngBounds(mapBounds);

        // leafletMap.on('click', (e) => {
        //     let popup = L.popup();
        //     popup
        //         .setLatLng(e.latlng)
        //         .setContent("You clicked the map at " + e.latlng.toString())
        //         .openOn(leafletMap);
        // });
        // updateBounds();
    }
};
const updateBounds = () => {
    // todo: map連動table
    const leafletMap = map.value.leafletObject;

    let mapBounds = leafletMap.getBounds();
    let newBounds = {
        lon: [mapBounds.getWest(), mapBounds.getEast()],
        lat: [mapBounds.getSouth(), mapBounds.getNorth()]
    },
        originBounds = mapEvent.originBounds ?? newBounds;

    Object.assign(mapEvent, {
        bounds: newBounds,
        // mapShift: originBounds ? newBounds.lon[1] - originBounds.lon[1] : 0,
    })
    // console.debug(newBounds.lon);
};
</script>

<template>
    <div :class="`leafletMap ${icons.expand.flag ? 'expand' : 'shrink'}`">
        <!-- 正中間：[0,0] -->
        <LMap ref="map" :center="mapCenter" :zoom="7" :zoomAnimation="false" @ready="readyHandler"
            @update:bounds="updateBounds()">
            <LControlLayers :disableScrollPropagation="true" />
            <!--layer-type=" base" for LControlLayers -->
            <LTileLayer v-for="mapState in tileProviders" layer-type="base" :minZoom="5" :key="mapState.name"
                :url="mapState.url" :attribution="mapState.attribution" :name="mapState.name"
                :maxZoom="mapState.maxZoom" :visible="mapState.name === defaultTile" :noWrap="false" :options="{
        // keepBuffer: Infinity
    }" />
            <component :is="clusterFlag ? MarkerCluster : 'div'" :options="clusterFlag ? {
        showCoverageOnHover: true,
        chunkedLoading: true,
        // zoomToBoundsOnClick: false,
        spiderLegPolylineOptions: { weight: 3, color: '#FFF', opacity: 1 },
        // disableClusteringAtZoom: 2,
        // singleMarkerMode: true,
        // animateAddingMarkers: true,
    } : false" ref="cluster">
                <slot name="mapLayers"></slot>
            </component>
        </LMap>
        <mapControllerUI v-if="!(mapName === 'dataStaMap')" :mapController="props.mapController" :theme="theme">
        </mapControllerUI>
    </div>
</template>

<style scoped>
.leafletMap {
    position: sticky;
    /* height: 780px; */
    height: 85vh;
    top: 0;
}

.leafletMap.shrink {
    max-width: 1024px;
}


:deep(.leaflet-popup-content) {
    white-space: nowrap;
}

text,
label,
font,
div,
h1,
h2,
h3 {
    user-select: none;
}
</style>@/components/statics/tileProviders