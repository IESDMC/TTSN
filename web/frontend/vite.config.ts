import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  base: "./",
  build: {
    assetsDir: "static",
    // rollupOptions: {
    //   output: {
    //     assetFileNames: (assetInfo) => {
    //       let extType = assetInfo.name.split(".").slice(-1)[0];
    //       if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
    //         extType = "img";
    //       }
    //       // console.log(assetInfo.name, extType);
    //       return `static/${extType}/[name]-[hash][extname]`;
    //     },
    //     chunkFileNames: "static/js/[name]-[hash].js",
    //     entryFileNames: "static/js/[name]-[hash].js",
    //   },
    // },
  },
});
