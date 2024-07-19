import gql from "graphql-tag";

export const queryStations = gql`
  query {
    TTSN {
      stationList {
        elev
        gain
        lat
        lon
        nameChinese
        nameEnglish
        stationCode
      }
    }
  }
`;

export const queryData = gql`
  query {
    TTSN {
      dataList {
        component
        date
        fileName
        station
      }
    }
  }
`;

export const queryDataFile = gql`
  query ($yearObj: JSON, $fileType: dataFile_choices) {
    TTSN {
      dataFile(fileType: $fileType, yearObj: $yearObj) {
        data
        name
      }
    }
  }
`;
