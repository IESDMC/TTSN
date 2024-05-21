import gql from "graphql-tag";

export const queryStations = gql`
  query {
    stationList {
      elev
      gain
      lat
      nameChinese
      lon
      nameEnglish
      stationCode
    }
  }
`;

export const queryData = gql`
  query {
    dataList {
      component
      date
      fileName
      station
    }
  }
`;

export const queryDataFile = gql`
  query ($yearObj: JSON, $fileType: dataFile_choices) {
    dataFile(fileType: $fileType, yearObj: $yearObj) {
      data
      name
    }
  }
`;
