import "@fortawesome/fontawesome-free/css/all.min.css";
import { BootstrapVue3 } from "bootstrap-vue-3";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";
import "bootstrap/dist/css/bootstrap.css";
import { createPinia } from "pinia";
import piniaPersist from "pinia-plugin-persist";
import { createApp } from "vue";
import App from "./App.vue";
import i18n from "./i18n";
import router from "./router";

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPersist);

app.use(pinia).use(router).use(BootstrapVue3).use(i18n).mount("#app");
