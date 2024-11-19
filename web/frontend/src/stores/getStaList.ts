// @ts-check
import axiosAPI from "@/axios-auth";
import type { stationListType } from "@/components/statics/types";
import { print } from "graphql";
import { defineStore } from "pinia";
import { ref } from "vue";
import { queryStations } from "./schema/query";

export const useStaListStore = defineStore("stationList", () => {
  //==state
  const staList = ref<stationListType>();
  //==action
  const getStaList = () => {
    axiosAPI
      .post("graphql/", {
        query: print(queryStations),
      })
      .then((response) => {
        // console.log("TTSN.stationList=", response.data.data.TTSN.stationList);
        let tmp: Array<{
          stationCode: string;
          nameChinese: string;
          nameEnglish: string;
          elev: number;
          gain: number;
          lat: number;
          lon: number;
        }> = response.data.data.TTSN.stationList;

        let list: stationListType = tmp.map((obj) => {
          let nObj = Object.assign(obj, {
            station: obj["stationCode"].trim(),
          });
          delete obj["stationCode"];
          return nObj;
        });

        // tmp.staInfos = tmp.staInfos.filter((sta) => {
        //   let isOnline = true;
        //   if (staFilter === "history") {
        //     isOnline = (function () {
        //       let end = new Date(`${sta.end_at}T24:00:00Z`).getTime();
        //       let now = new Date().getTime();
        //       return end > now;
        //     })();
        //   }
        // sta.isOnline = isOnline;
        //   return historyOnly ? !isOnline : true;
        // });

        staList.value = list;
      })
      .catch((err) => {
        console.log(err);
      });
  };
  const resetState = () => {
    // staList.value = {};
    Object.assign(staList, ref<stationListType>());
    console.debug("clean state");
  };
  return { getStaList, resetState, staList };
});
