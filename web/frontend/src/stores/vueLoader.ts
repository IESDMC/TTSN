// @ts-check
import { defineStore } from "pinia";
import { ref } from "vue";

export const useVueLoaderStore = defineStore("vueLoader", () => {
  //==state
  const loaderActive = ref<boolean>(false);
  //==action
  const setActive = (active: boolean) => {
    // console.debug("vueLoader active=", active);
    loaderActive.value = active;
  };

  return {
    loaderActive,
    setActive,
  };
});
