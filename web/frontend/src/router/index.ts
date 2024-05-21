import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/homeView.vue"),
    },
    {
      path: "/station",
      name: "station",
      component: () => import("@/views/stationView.vue"),
    },
    {
      path: "/data",
      name: "data",
      component: () => import("@/views/dataView.vue"),
    },
    {
      path: "/help",
      name: "helpPage",
      component: () => import("@/views/helpPageView.vue"),
    },
  ],
});

export default router;
