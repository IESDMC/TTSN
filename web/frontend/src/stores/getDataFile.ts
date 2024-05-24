// @ts-check
import axiosAPI from "@/axios-auth";
import type { dataListType, fileDataType } from "@/components/statics/types";
import { print } from "graphql";
import { defineStore } from "pinia";
import { ref } from "vue";
import { queryDataFile } from "./schema/query";

// let axiosAPI = null;
export const useDataFileStore = defineStore("dataFileStore", () => {
  const fileData = ref<fileDataType>();
  const userDownloadList = ref<dataListType>([]);

  function getYearObj(dataList) {
    let yearObj = dataList.reduce((acc: { [key: string]: string[] }, obj) => {
      const key = obj["date"].split("-")[0];
      const fileArr = acc[key] ?? [];
      fileArr.push(obj["fileName"]);
      return { ...acc, [key]: fileArr };
    }, {});

    return yearObj;
  }
  //==action
  const getZipFile = (dataList: dataListType) => {
    let yearObj = getYearObj(dataList);
    let params = { yearObj };
    // console.debug(params);

    axiosAPI
      .post("download/", params, { responseType: "blob" })
      .then((response) => {
        // console.log(response);
        // create file link in browser's memory
        const href = URL.createObjectURL(response.data);
        // create "a" HTML element with href to file & click
        const link = document.createElement("a");
        Object.assign(link, {
          href,
          download: `TTSN.${new Date().toISOString()}.zip`,
        });
        // link.href = href;
        // link.setAttribute("download", "file.tgz"); //or any other extension
        document.body.appendChild(link);
        link.click();

        // clean up "a" element & remove ObjectURL
        document.body.removeChild(link);
        URL.revokeObjectURL(href);

        console.log("Download Success!");
      })
      .catch((err) => {
        console.log(err);
      });
  };
  const getImgFile = (type: number, dataList: dataListType) => {
    // console.debug(type, dataList);
    let fileType = ["jpg", "zip"][type],
      yearObj = getYearObj(dataList);

    let params = { yearObj, fileType };
    // console.debug(params);
    return new Promise((resolve, reject) => {
      axiosAPI
        .post("graphql/", {
          query: print(queryDataFile),
          variables: params,
        })
        .then((response) => {
          // console.debug(response);
          function base64ToByteArray(base64Data) {
            let byteCharacters = atob(base64Data),
              buffer = new Array(byteCharacters.length),
              byteArray = new Uint8Array(buffer);
            for (let i = 0; i < byteCharacters.length; i++) {
              byteArray[i] = byteCharacters.charCodeAt(i);
            }
            // console.debug(byteNumbers, byteArray);
            return byteArray;
          }
          let tmp = response.data.data.dataFile[0];
          let base64Data = tmp.data;
          // console.debug(tmp);

          switch (fileType) {
            case "jpg":
              const mimeType = "image/jpg";
              fileData.value = {
                data: `data:${mimeType};base64,${base64Data}`,
                onClick: (e) => {
                  function openBase64InNewTab(data, mimeType) {
                    let byteArray = base64ToByteArray(data);
                    let file = new Blob([byteArray], {
                      type: mimeType + ";base64",
                    });
                    let fileURL = URL.createObjectURL(file);
                    window.open(fileURL);
                  }
                  openBase64InNewTab(base64Data, mimeType);
                },
              };
              break;
            case "zip":
              const href = `data:application/zip;base64,${base64Data}`;
              // create "a" HTML element with href to file & click
              const link = document.createElement("a");
              Object.assign(link, {
                href,
                download: `TTSN.${new Date().toISOString()}.zip`,
              });
              document.body.appendChild(link);
              link.click();

              // clean up "a" element
              document.body.removeChild(link);

              console.log("Download Success!");
              break;
          }

          resolve(fileData.value);
        })
        .catch((err) => {
          console.log(err);
        });
    });
  };

  const resetState = () => {
    fileData.value = undefined;
    // console.debug("clean state");
  };

  return {
    getImgFile,
    getZipFile,
    fileData,
    resetState,
  };
});
