import { useVueLoaderStore } from "@/stores/vueLoader";
import axios from "axios";

// const ttsnAPI = "https://tecdc.earth.sinica.edu.tw/";
const ttsnAPI = "http://140.109.80.59:8000/";

const instance = axios.create({
  baseURL: ttsnAPI,
  // headers: {
  //   "Content-Type": "application/json",
  // },
  // responseType: "blob",
});

// Add a request interceptor
const VueLoaderStore = useVueLoaderStore();
instance.interceptors.request.use(
  (req) => {
    // Do something before request is sent
    // console.debug(req);
    VueLoaderStore.setActive(true);
    // const JWT = store.getters.getJWT
    // JWT && (x.headers.Authorization = 'JWT ' + JWT)
    return req;
  },
  function (error) {
    // Do something with request error
    VueLoaderStore.setActive(false);
    return Promise.reject(error);
  }
);

// Add a response interceptor
instance.interceptors.response.use(
  function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    VueLoaderStore.setActive(false);
    return response;
  },
  function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    VueLoaderStore.setActive(false);
    // console.log('ERROR in response')
    return Promise.reject(error);
  }
);

export default instance;
