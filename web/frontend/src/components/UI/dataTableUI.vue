<script setup lang="ts">
import type { staInfoType, UIControlsType } from "@/components/statics/types";
import { useDataFileStore } from "@/stores/getDataFile";
import { useVueLoaderStore } from "@/stores/vueLoader";
import { reactive, ref, watch, type PropType } from "vue";
import { VueGoodTable } from 'vue-good-table-next';
import "vue-good-table-next/dist/vue-good-table-next.css";
import { useI18n } from 'vue-i18n';

const dataTable = ref(null);
const { t, locale } = useI18n({ inheritLocale: true });
const VueLoaderStore = useVueLoaderStore();

const props = defineProps({
  UIControls: {
    type: Object as PropType<UIControlsType<staInfoType>>,
    required: true,
  },
  dataList: {
    type: Object as PropType<staInfoType[] | any[]>,
    required: false,
  }
});
const tableTarget = props.UIControls.tableTarget;
const dialogControls = props.UIControls.dialogUI;
const others = props.UIControls.others;

const tableData = reactive<{ columns: any[], rows: any[], disabledRow: any }>
  ({ columns: [], rows: [], disabledRow: undefined });

const getCol = (type: string) => {
  let col: any[];
  switch (type) {
    case 'station':
      col = [
        {
          label: t('station'),
          field: 'station',
          sortable: true,
          firstSortType: 'desc'
        },

        {
          label: t('stationName'),
          field: locale.value === "tw" ? 'nameChinese' : 'nameEnglish',
          type: 'string',
        },
        {
          label: t('latitude') + " (°)",
          field: 'lat',
          type: 'number',
          formatFn: (value: number) => `${(+value).toFixed(4)}`,
        },
        {
          label: t('longitude') + " (°)",
          field: 'lon',
          type: 'number',
          formatFn: (value: number) => `${(+value).toFixed(4)}`,
        },
        {
          label: t('elev') + " (m)",
          field: 'elev',
          type: 'number',
        },
        {
          label: t('gain'),
          field: 'gain',
          type: 'number',
        },
      ];
      break;
    case 'data':
      col = [
        {
          label: t('date'),
          field: 'date',
          sortable: true,
          firstSortType: 'desc'
        },
        {
          label: t('station'),
          field: 'station',
          type: 'string',
        },
        {
          label: t('component'),
          field: 'component',
          type: 'string',
        },
        {
          label: t('fileName'),
          field: 'fileName',
          type: 'string',
          tdClass: 'td_link',
        },

      ];
      break;
    case 'downloadLog':
      col = [
        {
          label: t('download_affiliation'),
          field: 'affiliation',
          type: 'string',
        },
        {
          label: t('download_email'),
          field: 'email',
          type: 'string',
        },
        {
          label: t('download_sizeMB'),
          field: 'sizeBytes',
          type: 'number',
          formatFn: (value: number) => (value / 1024 / 1024).toFixed(2),
        },
      ];
      break;
    default:
      col = []
      break;
  };
  // console.debug('type', tableTarget);

  return col;
};
watch(() => tableTarget.type, (type) => {
  // console.debug('type', type, tableData);
  tableData.columns = getCol(type);

  switch (type) {
    case 'event':
      tableData.disabledRow = {
        key: 'hasPGA',
        funArray: [(val: any) => !val],
      };
      break;
    case 'stationPga':
    case 'eventPga':
      tableData.disabledRow = {
        key: 'pga',
        funArray: [(val: null) => val === null, (val: number) => val < 0],
      };
      break;
    default:
      tableData.disabledRow = null;
      break;
  };

}, { immediate: true });
watch(() => props.dataList, (list) => {
  // console.debug('props.dataList', list);
  if (!list) return;
  // VueLoaderStore.setActive(true);
  tableData.rows = list;
});

//==js生成的節點要手動更新
watch(locale, () => {
  tableData.columns = getCol(tableTarget.type);
});

const downloadCSV = () => {
  const columns = tableData.columns.map(col => col.field),
    rows = tableData.rows;
  // console.debug(columns, rows);

  let csvContent = columns.join(',') + '\n';
  rows.forEach(row => {
    let rowData = columns.map(col => {
      let val = row[col];
      val = String(val).includes(",") ? `"${val}"` : val;
      return val;
    });
    csvContent += rowData.join(',') + '\n';
  });

  // 下載的檔案名稱
  let fileName = new Date().toISOString() + '.csv';

  // 建立一個 a，並點擊它
  let link = document.createElement('a');
  Object.assign(link, {
    href: 'data:text/csv;charset=utf-8,%EF%BB%BF' + encodeURI(csvContent),
    download: fileName,
  });
  link.click();
  link.remove();
};
const downloadData = {
  maxSelection: 50,
  overLimitFlag: () => dataTable.value && (dataTable.value.selectedRows.length > downloadData.maxSelection),
  //for disable download
  disableButton: () => dataTable.value && (!dataTable.value.selectedRows.length || downloadData.overLimitFlag()),
  download: () => {
    let table = dataTable.value;
    console.debug("table=", table);

    let overLimitFlag = downloadData.overLimitFlag();
    if (overLimitFlag) return;
    const dataFileStore = useDataFileStore();
    dataFileStore.getZipFile(table.selectedRows);
  },
  // 檢查選擇數量
  checkAmount: () => {
    // await autoSelectAll;
    let selectInfo = dataTable.value.$el.querySelector('.selectionInfo');
    // console.debug("table=", table);
    // console.debug("selectedRows=", table.selectedRows.length);

    let showSelectedRows = () => {
      let rowCount = dataTable.value.selectedRows.length;
      selectInfo.querySelector('.selectedRowCount').innerText = t("rowsSelected", { val: rowCount });
    }
    let triggerWarning = (flag) => {
      let warning = selectInfo.querySelector('.selectWarning');
      warning.style.display = flag ? "block" : "none";
    };
    showSelectedRows();
    triggerWarning(downloadData.overLimitFlag());
  },
  selectAll: (flag) => {
    let table = dataTable.value;
    table.filteredRows.forEach((headerRow, i) => {
      headerRow.children.forEach((row, j) => {
        row["vgtSelected"] = flag;
      });
    });
    table.emitSelectedRows();
  }
  // console.debug(dialogControls)
  // Object.assign(dialogControls.content, {
  //   type: 'downloadForm',
  //   data: {
  //   }
  // });
  // return;

};

const rowStyleClassFn = (row: any) => {
  let classList = 'tableRow';
  if (tableData.disabledRow) {
    //==有判斷資料不齊的欄位名&&該row的資料值不從再&&資料值不爲0
    let disabledKey = tableData.disabledRow.key,
      funArray = tableData.disabledRow.funArray;
    funArray.forEach((fun: (arg0: any) => any, idx: number) =>
      classList += fun(row[disabledKey]) ? ` disabledRow${idx + 1}` : '');
  };
  return classList;
};

</script>

<template>
  <VueGoodTable :styleClass="`vgt-table text-nowrap
  `" :columns="tableData.columns" :rows="tableData.rows" :row-style-class="rowStyleClassFn" :sort-options="{
    enabled: true,
    initialSortBy: {
      field: tableData.columns[0]?.field, type: 'asc'
    },
  }" :pagination-options="{
    enabled: true,
    mode: 'pages',
    // totalRows: 999,
    nextLabel: $t('tableNext'),
    prevLabel: $t('tablePrev'),
    rowsPerPageLabel: $t('tableRowsPerPage'),
    ofLabel: $t('tableOf'),
    pageLabel: $t('tablePage'), // for 'pages' mode
    allLabel: $t('tableAll'),
    // infoFn: (params) => `my own page ${params.firstRecordOnPage}`,
  }" :search-options="{ enabled: true }" @row-mouseenter="(params: any) => tableTarget.hovered = params"
    @row-mouseleave="() => (tableTarget.hovered = undefined)" @row-click="(params: any) => tableTarget.clicked = params"
    @selected-rows-change="downloadData.checkAmount" :select-options="{
    enabled: tableTarget?.action === 'download',
    disableSelectInfo: true,
    // selectionInfoClass: 'selectionInfo',
    // selectionText: $t('rowsSelected'),
    // clearSelectionText: $t('clear'),
  }" ref="dataTable">
    <template #table-actions>
      <div class="d-flex flex-column">
        <div class="d-flex flex-row-reverse">
          <div class="downloadBtns">
            <button type="button" :title="$t('downloadCSV')" class="btn btn-secondary me-2" @click="downloadCSV()"
              :disabled="!tableData.rows.length">
              {{ $t("downloadCSV") }}
            </button>
            <button v-if="tableTarget?.action === 'download'" type="button" :title="$t('downloadData')"
              class="btn btn-secondary me-2" @click="downloadData.download()"
              :disabled="!tableData.rows.length || downloadData.disableButton()">
              {{ $t("downloadData") }}
            </button>
          </div>
        </div>
        <div v-if="tableTarget?.action === 'download'" class="selectionInfo d-flex flex-nowrap">
          <div class="selectedRowCount me-3">{{ $t("rowsSelected", { val: 0 }) }}</div>
          <div v-show="false" class="selectWarning">{{ $t("selectWarning") }}</div>
          <div class="position-absolute end-0">
            <button class="btn btn-secondary me-2" @click="downloadData.selectAll(true)">{{ $t("selectAll") }}</button>
            <button class="btn btn-secondary me-2" @click="downloadData.selectAll(false)">{{ $t("unselectAll")
              }}</button>
          </div>
        </div>
      </div>
    </template>
    <template #table-actions-bottom>

      <!-- 表格背景灰色爲資料不齊全 -->
      <div v-if="tableData.disabledRow">
        <div class="d-flex flex-row flex-nowrap">
          <span>{{ `${$t("tableRowDetail")} ` }}</span>
          <ol>
            <!-- <li>{{ $t("tableRowDetail1A") }}</li> -->
            <li v-for="(fun, idx) in tableData.disabledRow.funArray" :class="`disabled_li${idx + 1}`">
              {{ $t(`tableRowDetail_${tableData.disabledRow.key === 'pga' ? 'B' : 'A'}_${idx}`) }}
            </li>
          </ol>
        </div>
      </div>

      <!-- tableTotal -->
      <div class="d-flex flex-row-reverse">
        <label class="total_label">{{
    `${$t("tableTotal")} : ${tableData.rows.length +
    (!isNaN(others?.tableAllStaTotal) ? (' / ' + others?.tableAllStaTotal) : '')} `
          }}</label>
      </div>
    </template>
  </VueGoodTable>
</template>

<style lang="scss" scoped>
:deep(#vgt-table) {
  &.nowrap {
    white-space: nowrap;
  }

}

:deep(.tableRow) {
  >th {
    border-bottom: 1px solid #dcdfe6;
    border-right: 1px solid #dcdfe6;
  }

  >td {
    border: unset;
    border-bottom: 1px solid #dcdfe6;

    &.td_link {
      color: #256fc7;
      text-decoration: underline;
      cursor: pointer;
    }
  }

  &:hover {
    background-color: palegoldenrod;
    // cursor: pointer;
  }
}



:deep(.total_label) {
  color: #606266;
  font-size: 1.5em;
  padding: 0 30px 0 10px;
}

// 搜尋列
:deep(.vgt-global-search) {
  padding: 10px 0;
  padding-bottom: 0;

  .vgt-global-search__input {
    width: 250px;
    flex-grow: unset;
    position: absolute;
  }

  .vgt-global-search__actions {
    width: 100%;
    margin-left: 0px;
  }

  .downloadBtns {
    // position: absolute;
    // right: 10px;
  }
}

// 表格說明
:deep(.vgt-wrap__actions-footer) {
  background: linear-gradient(#f8f8f8, #fafafa);
  padding: 10px;
  color: #606266;

  span {
    font-size: 1em;
  }

  ol {
    list-style: none;
    padding: 0;
  }

  li {
    position: relative;
    padding-left: 30px;
    font-size: 1em;
  }

  li::after {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translate(80%, -50%);
    width: 15px;
    height: 15px;

  }

  li.disabled_li1::after {
    background-color: rgb(177, 175, 175) !important;
  }

  li.disabled_li2::after {
    background-color: rgb(207, 207, 207) !important;
  }

}

:deep(.disabledRow1) {
  background-color: rgb(177, 175, 175) !important;

  td {
    opacity: 0.6;
  }
}

:deep(.disabledRow2) {
  background-color: rgb(207, 207, 207) !important;

  td {
    opacity: 0.6;
  }
}

:deep(.selectionInfo) {
  font-size: 24px;
  background: #fdf9e8;
  padding: 5px 16px;
  border-top: 1px solid #DCDFE6;
  color: #d3aa3b;
  font-weight: 700;
  margin-top: 10px;

  .selectWarning {
    color: rgb(197, 25, 25);
    font-weight: 700;
  }
}
</style>
