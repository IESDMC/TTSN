// @ts-check
import axiosAPI from "@/axios-auth";
import type { dataListType } from "@/components/statics/types";
import { print } from "graphql";
import { defineStore } from "pinia";
import { ref } from "vue";
import { queryData } from "./schema/query";

export const useDataListStore = defineStore("dataList", () => {
  //==state
  const dataList = ref<dataListType>();
  //==action
  const getDataList = () => {
    axiosAPI
      .post("graphql/", {
        query: print(queryData),
      })
      .then((response) => {
        console.debug(response.data.data.dataList);
        let tmp: dataListType = response.data.data.dataList;
        dataList.value = tmp;
      })
      .catch((err) => {
        console.log(err);
      });
  };
  const resetState = () => {
    // dataList.value = {};
    Object.assign(dataList, ref<dataListType>());
    console.debug("clean state");
  };
  return { getDataList, resetState, dataList };
});
