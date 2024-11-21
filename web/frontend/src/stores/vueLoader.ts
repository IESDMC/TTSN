// @ts-check
import { defineStore } from "pinia";
import { ref } from "vue";

export const useVueLoaderStore = defineStore("vueLoader", () => {
  //==state
  const loaderActive = ref<boolean>(false);
  const boolArr = ref<boolean[]>([]); //一次多個請求時用來判斷所有都完成
  //==action
  const setActive = (active: boolean) => {
    // if (active === false && requestArr.value.length !== 0) return;
    active ? boolArr.value.push(true) : boolArr.value.pop();
    console.debug("boolArr", boolArr.value);
    if (active === false && boolArr.value.length !== 0) return;
    loaderActive.value = active;
    // console.debug("vueLoader active=", loaderActive.value);
  };
  // const addXHR = (obj: any, isRequest = true) => {
  //   // console.debug(isRequest, obj);
  //   // req放進陣列，res用來找該次req並從陣列中刪除，
  //   if (isRequest) requestArr.value.push(obj);
  //   else {
  //     requestArr.value = requestArr.value.filter(
  //       (req) => !(req.data === obj.config.data)
  //     );
  //   }
  // };

  return {
    loaderActive,
    setActive,
  };
});
