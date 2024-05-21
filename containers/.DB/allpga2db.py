from datetime import datetime, timedelta
from glob import glob
from os.path import isdir, isfile

import pandas as pd
import requests

url = 'http://140.109.80.93:8003/graphql/'
dataDir = '/mnt/palertData/20*/20*'
# dataDir = '/mnt/palertData/2022/20220914013551'

query = """mutation MyMutation ($date: Date!, $time: Time!, $pga: Float, $dist: Float, $az:Float, $station:String!){
  authIes {
    ... on UpdateDB {
      __typename
      addPga(
        PGAInput: {date: $date, time: $time, pga: $pga, dist: $dist, az: $az, staCode: $station}
      ) {
        text
        success
      }
    }
    ... on GQLAuthError {
      __typename
      code
      message
    }
  }
}"""


def pga2db(data, date, time):
    df = pd.read_csv(data, sep=" ",
                     names=['sta', 'stla', 'stlo', 'az', 'dist', 'pga'],
                     skipinitialspace=True,
                     skiprows=[0])
    for row in df.itertuples():
        try:
            variables = {
                'station': str(row.sta),
                'az': row.az,
                'dist': row.dist,
                'pga': row.pga,
                'date': date,
                'time': time
            }
            r = requests.post(url, json={'query': query, "variables": variables})

            msg = str(r.json().get('data'))
            # print('variables=', variables)
            # print('msg=', msg)
            if ('None' in msg or 'False' in msg):
                with open('error.pga.log', mode='a') as f:
                    f.write(f'{str(row.sta)},{r.json().get("data")},{variables}\n')
            print(variables, r.json().get('data').get('authIes').get('addPga').get('text'))
        except:
            print('pga=', row.pga)
            pass

# def toTwTime(timeString):  # cwb_report用臺灣時間
#     # timeString format : 2022-07-26T09:38:21.812Z
#     struct_time = datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)
#     return struct_time.isoformat()


for eventPath in (x for x in glob(dataDir)):
    dateStr = eventPath.split("/")[-1].lower()

    pga = f'{eventPath}/{dateStr}_PGA.txt'
    # eventList = f'{eventPath}/eventlist.txt'
    # print(dateStr)
    [date_, time_] = [f'{dateStr[0:4]}-{dateStr[4:6]}-{dateStr[6:8]}',
                      f'{dateStr[8:10]}:{dateStr[10:12]}:{dateStr[12:14]}']
    # print(date_, time_)
    # if isfile(eventList):
    #     with open(eventList, mode='r') as f:
    #         [date, time, *tmp] = f.readline().strip().split(" ")
    #     date_ = date.replace("/", "-")
    #     time_ = time.split(".")[0]
    #     # print(date_, time_)
    #     # datetime_ = toTwTime(f'{date_}T{time_}').split("T")
    #     # [date_, time_] = datetime_
    # else:
    #     continue

    if isfile(pga):
        pga2db(pga, date_, time_)
