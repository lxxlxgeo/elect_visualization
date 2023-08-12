# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 2:59

@author: lxce
"""
# %%
import datetime
import re
import h5py
import numpy as np
import xarray as xr
from un_config.cldas_config import cldas_path, extent
from glob import glob


# %%
class Cldas_Reader(object):
    def __init__(self, start_time, end_time, step):
        """
        :param start_time: 实况场初始时间,实况数据没有初始场的概念
        :param end_time: 实况结束时间
        :param step: 计算步长
        :return: None
        """
        self.filepath = cldas_path
        self.start_time: datetime.datetime = start_time
        self.end_time: datetime.datetime = end_time
        self.step = step
        self.extent = extent
        self.time_list = self.__get_initial__info()

    def __get_initial__info(self):
        """
        这里规定,如果间隔时常为24小时的话，开始时间到结束时间不足
        :return:
        """
        # time_length=self.end_time-self.start_time
        time_length = self.end_time - self.start_time
        days = time_length.days
        seconds = time_length.seconds
        hours = days * 24 + seconds / 3600
        if hours % self.step != 0:
            print("当前实况结束时间设置错误，已自动更正")
            self.end_time = self.start_time + datetime.timedelta(hours=(days * 24 + self.step))
            # 如果是预报的话，这里需要控制时长，避免超过预报的时长
            print("新的结束时间为:{}".format(self.end_time.strftime('%Y-%m-%d-%H')))
            self.d_time = int(hours / self.step)
            time_list = []
            for i in range(self.d_time):
                item_time = self.start_time + datetime.timedelta(hours=(i * self.step))
                time_list.append(item_time)
            return time_list
        else:
            self.d_time = int(hours / self.step)
            time_list = []
            for i in range(self.d_time):
                item_time = self.start_time + datetime.timedelta(hours=(i * self.step))
                time_list.append(item_time)
            return time_list

    def get_data(self, attr: str, attribute, method):

        ##文件名变量
        """
        p_filename=['WIND','PRE']
        #内容变量
        p_context=['PRCP','WIND']
        :param attr:
        :return:
        """
        data_list = []
        for forecast_start_time in self.time_list:
            data_dict = dict()
            forecast_end_time = forecast_start_time + datetime.timedelta(hours=self.step)
            # 获取当前时段的文件夹里的内容
            files = self.find_files(forecast_start_time, attr)
            data, lon, lat = composite_data(files, attribute, method)
            data_dict['data'] = data
            data_dict['lon'] = lon
            data_dict['lat'] = lat
            data_dict['forecast_start_time'] = forecast_start_time
            data_dict['forecast_end_time'] = forecast_end_time
            data_list.append(data_dict)
        return data_list

        # print("时段:{}-{}".format(forecast_start_time,forecast_end_time))

    def find_files(self, forecast_time, attr: str):
        # d_time=self.step
        # forecast_time 为某个时段的初始时间,这里不容易读懂,需要改进
        start_time = forecast_time
        file_list = []
        for i in range(self.step):
            temp_time_str = (start_time + datetime.timedelta(hours=i + 1)).strftime('%Y%m%d%H')
            # 暂时先这样吧,以后再改
            file = glob(self.filepath + '\\*-{attr}-{time_str}_*.nc'.format(attr=attr, time_str=temp_time_str))
            if len(file) > 0:
                file_list.append(file[0])
            else:
                print("当前时段:{} 没有数据,可能造成计算错误".format(temp_time_str))
                continue
        return file_list


# 文件名变量
# p_filename=['WIND','PRE']
# #内容变量
# p_context=['PRCP','WIND']
def composite_data(files: list, attribute: str, method: str):
    """
    :param files: 文件列表
    :param attribute: nc文件属性
    :param method: 合成方式
    :return:
    """

    stack_array = np.array([], dtype=np.float32)
    for file in files:
        ds = xr.open_dataset(file)
        # lon,lat=
        lat = ds['LAT'].loc[extent[2]:extent[3]]
        lon = ds['LON'].loc[extent[0]:extent[1]]
        data_array = ds[attribute][:, :].sel(LAT=slice(extent[2], extent[3]), LON=slice(extent[0], extent[1]))
        if len(stack_array) == 0:
            stack_array = data_array
        else:
            stack_array = np.dstack((stack_array, data_array))

    if method == 'max':
        result_array = np.nanmax(stack_array, axis=2)
        return result_array, lon, lat
    if method == 'sum':
        result_array = np.sum(stack_array, axis=2)
        return result_array, lon, lat
    if method == 'avg':
        result_array = np.nanmean(stack_array, axis=2)
        return result_array, lon, lat


# attr=['WIND','PRE']
def convert_utc2btj(utc_time: datetime.datetime):
    btj_time = utc_time + datetime.timedelta(hours=8)
    return btj_time


def convert_btj2utc(btj_time: datetime.datetime):
    utc_time = btj_time + datetime.timedelta(hours=-8)


# if __name__ == '__main__':
#     clds = Cldas_Reader(start_time=datetime.datetime(2023, 8, 4, 12), end_time=datetime.datetime(2023, 8, 6, 12),
#                         step=24)
#     pre_data_list = clds.get_data('PRE', 'PRCP', 'sum')
#     print(pre_data_list)
