from datetime import datetime, timedelta
from glob import glob
from os.path import isdir, isfile

import pandas as pd
import requests

url = 'http://140.109.80.93:8003/graphql/'
dataDir = '/home/andy/html/Web/Palert/palert_vite/.backup/sql/pga2db_202209-12.csv'
# palert2_evt2db

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


def csv2db(data):
    df = pd.read_csv(data, sep=",",
                     names=['id', 'event', 'staCode', 'pga', 'az', 'dist', 'timestamp'],
                     #  dtype={'id': 'int', 'event': 'str', 'staCode': 'str',
                     #         'pga': 'float', 'az': 'float', 'dist': 'float'}
                     #  dtype=[int, datetime, str, float, float, float, datetime],
                     skipinitialspace=True,
                     header=None)
    # print(df)
    # return
    for row in df.itertuples():
        try:
            [date_, time_] = row.event.split(" ")
            variables = {
                'station': str(row.staCode),
                'az': float(row.az),
                'dist': float(row.dist),
                'pga': float(row.pga),
                'date': str(date_),
                'time': str(time_)
            }
            r = requests.post(url, json={'query': query, "variables": variables})

            msg = str(r.json().get('data'))
            # print('variables=', variables)
            # print('msg=', msg)
            # if ('None' in msg or 'False' in msg):
            #     with open('error.csv2pga.log', mode='a') as f:
            #         f.write(f'{str(row.staCode)},{r.json().get("data")},{variables}\n')
            print(variables)
            # print(variables, r.json().get('data').get('authIes').get('addPga').get('text'))
        except Exception as ex:
            print(ex)
            # print('pga=', row.pga)
            pass


csv2db(dataDir)
