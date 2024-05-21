//=== data type
export type staInfoType = {
  station: string;
  nameChinese: string;
  nameEnglish: string;
  elev: number;
  gain: number;
  lat: number;
  lon: number;
};
export type stationListType = staInfoType[];

export type dataType = {
  station: string;
  date: string;
  fileName: string;
  component: string;
};
export type dataListType = dataType[];

//=== UI type
export type tableRowType<T> = {
  event: Event;
  pageIndex: number;
  row: T;
  selected: boolean;
};

export type tableTargetType<T> = {
  hovered?: tableRowType<T>;
  clicked?: tableRowType<T>;
  type: string;
  action?: string;
  selectFlag?: boolean;
};
export type dialogUIType = {
  openState: boolean;
  maxWidth: number;
  content: {
    type: string;
    data: dataType;
  };
};
export type UIControlsType<T = any> = {
  tableTarget: tableTargetType<T>;
  dialogUI?: dialogUIType;
  others?: { [key: string]: any };
};
export type downloadLogType = {
  affiliation: string;
  email: string;
  sizeBytes: number;
};
export type downloadLogDataType = {
  totalSize: number;
  logs: downloadLogType[];
};
//===waveformType
type Base64 = string;
export type fileDataType = {
  data: Base64;
  onClick?: (e: PointerEvent) => void;
};

//===vue
//todo:any改成清楚定義
export type mapControllerType = {
  icons: {
    [key: string]: any;
    criteria?: any;
    display?: any;
    lockView?: any;
    play?: any;
  };
  legend?: any;
  mapEvent: any;
  mapName: string;
  theme?: string;
};

//===Color
type RGB = `rgb(${number}, ${number}, ${number})`;
type RGBA = `rgba(${number}, ${number}, ${number}, ${number})`;
type HEX = `#${string}`;

export type Color = RGB | RGBA | HEX;
