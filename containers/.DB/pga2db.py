#!/usr/bin/env python3

from os.path import isdir, isfile
from subprocess import getstatusoutput

import numpy as np
import pandas as pd
import requests

url = 'http://140.109.82.114:8000/graphql/'
# url = 'http://140.109.80.93:8003/graphql/'
query = """mutation MyMutation($date: Date!, $time: Time!, $pga: Float, $dist: Float, $az: Float, $station: String!, $pgv: Float ) {
  authIes {
    ... on GQLAuthError {
      message
      code
    }
    ... on UpdateDB {
      __typename
      addPga(
        PGAInput: {date: $date, time: $time, pga: $pga, dist: $dist, az: $az, staCode: $station, pgv: $pgv}
      ) {
        success
        text
      }
    }
  }
}"""
query_delete = """mutation MyMutation($event: DateTime) {
  authIes {
    ... on UpdateDB {
      __typename
      deletePgaEvent(EventInput: {event: $event}) {
        success
        text
      }
    }
  }
}"""


def pga2db(data, date, time):
    df = pd.read_csv(data, sep=" ",
                     names=['sta', 'stla', 'stlo', 'az', 'dist', 'pga', 'pgv'],
                     skipinitialspace=True,
                     skiprows=[0])

    r = requests.post(url, json={'query': query_delete, "variables": {'event': f'{date} {time}'}})

    for row in df.itertuples():
        try:
            variables = {
                'station': str(row.sta),
                'az': row.az,
                'dist': row.dist,
                'date': date,
                'time': time
            }
            if (not np.isnan(row.pgv)):
                variables.update({'pgv': row.pgv})
            if (not np.isnan(row.pga)):
                variables.update({'pga': row.pga})

            r = requests.post(url, json={'query': query, "variables": variables})

            msg = str(r.json().get('data'))
            # print('variables=', variables)
            # print('msg=', r.json())
            if ('None' in msg or 'False' in msg):
                with open('error.pga.log', mode='a') as f:
                    f.write(f'{str(row.sta)},{r.json().get("data")},{variables}\n')
            print(variables, r.json().get('data').get('authIes').get('addPga').get('text'))
        except:
            # print('pga=',  f'{row.pga:.6f}')
            # print('pga=', row.pga)
            print('pga=', msg)
            pass


def main():
    _, path = getstatusoutput('pwd')
    dateStr = path.split("/")[-1].lower()

    pga = f'./{dateStr}_PGA.txt'
    [date_, time_] = [f'{dateStr[0:4]}-{dateStr[4:6]}-{dateStr[6:8]}',
                      f'{dateStr[8:10]}:{dateStr[10:12]}:{dateStr[12:14]}']

    # print('dateStr=', dateStr,date_, time_)

    if isfile(pga):
        pga2db(pga, date_, time_)


if __name__ == '__main__':
    main()
