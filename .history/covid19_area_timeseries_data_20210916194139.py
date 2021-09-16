import requests
import json
import pandas as pd
import time
import numpy as np
import datetime
import getAreaData


def local_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


if __name__ == '__main__':
    # getAreaData.writeRawData()
    rawData = pd.read_excel('rawData.xlsx', dtype={'date': str, 'y': str})
    cities = rawData[['province', 'city']].drop_duplicates()
    rawData['realdate'] = (rawData['y'] + rawData['date']).str.replace('.', '')
    rawData['realdate'] = pd.to_datetime(rawData.realdate)
    times = pd.date_range(start=min(rawData['realdate']),
                          end=max(rawData['realdate']))

    # 目的是做一个笛卡尔积，后来发现好像有crosstab这个函数
    t = pd.DataFrame(times, columns=['times'])
    t['as_key'] = 1
    cities['as_key'] = 1
    to_fill_table = cities.merge(t, how='left', on='as_key')
    del to_fill_table['as_key']

    to_fill_table.rename(columns={'times': 'realdate'}, inplace=True)
    filled_table = to_fill_table.merge(rawData,
                                       how='left',
                                       on=['province', 'city', 'realdate'])
    filled_table[filled_table['realdate'] > '2020-01-28']
    del filled_table['Unnamed: 0']
    del filled_table['y']
    del filled_table['date']

    today = time.strftime("%Y-%m-%d", time.localtime())
    filled_table = filled_table[filled_table['realdate'] <= today]

    filled_table.set_index(['province', 'city'], inplace=True)
    test = filled_table.groupby(['province', 'city']).ffill()
    del test['confirm_add']
    test = test.fillna(0)
    # localtime = local_timestamp()
    # test.to_csv('timeseriesData_'+localtime+'.csv',encoding='utf-8-sig')

    filled_table = test
    filled_table['yesterday'] = filled_table['realdate'] + datetime.timedelta(
        days=-1)
    cal_add_cross = filled_table.merge(
        filled_table,
        how='left',
        left_on=['province', 'city', 'yesterday'],
        right_on=['province', 'city', 'realdate'])
    cal_add_cross['confirm_cal_add'] = cal_add_cross[
        'confirm_x'] - cal_add_cross['confirm_y']
    cal_add_cross['suspect_cal_add'] = cal_add_cross[
        'suspect_x'] - cal_add_cross['suspect_y']
    cal_add_cross[
        'dead_cal_add'] = cal_add_cross['dead_x'] - cal_add_cross['dead_y']
    cal_add_cross[
        'heal_cal_add'] = cal_add_cross['heal_x'] - cal_add_cross['heal_y']
    cal_add_cross = cal_add_cross[[
        'realdate_x', 'confirm_x', 'dead_x', 'heal_x', 'suspect_x',
        'confirm_cal_add', 'suspect_cal_add', 'dead_cal_add', 'heal_cal_add'
    ]]
    cal_add_cross.rename(columns={
        'realdate_x': 'date',
        'confirm_x': 'confirm',
        'suspect_x': 'suspect',
        'dead_x': 'dead',
        'heal_x': 'heal'
    },
                         inplace=True)
    cal_add_cross.rename(columns={
        'confirm_cal_add': 'confrim_day_add',
        'suspect_cal_add': 'suspect_day_add',
        'dead_cal_add': 'dead_day_add',
        'heal_cal_add': 'heal_day_add'
    },
                         inplace=True)

    localtime = local_timestamp()
    cal_add_cross.to_csv('COVID-19_timeseriesData_Area_' + localtime + '.csv',
                         encoding='utf-8-sig')
    cal_add_cross.reset_index().to_excel('COVID-19_timeseriesData_Area_' +
                                         localtime + '.xlsx',
                                         encoding='utf-8-sig')
    # cal_add_cross.reset_index().to_excel('test.xlsx')
    print('Data Clean finish in ' + local_timestamp())
    print('COVID-19_timeseriesData_Area_' + localtime + '.csv (and .xlsx) has been written!')
