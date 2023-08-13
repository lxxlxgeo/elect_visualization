# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 8:17

@author: lixiang
"""
#%%
import numpy as np
import re
from glob import glob
import datetime
import xarray as xr
from un_config.rldas_configl import rldas_path,extent
from wrf import (get_cartopy, latlon_coords, to_np, cartopy_xlim, cartopy_ylim,
                 getvar, ALL_TIMES)

#%%

"""
RLDAS 模式数据读取,这里先改写一下:读取要素时初始化类还是直接从函数里获取????
"""
class RlDas_Reader(object):
    def __init__(self, start_time, end_time, step):
        # 开始时间
        self.start_time = start_time
        self.end_time = end_time  # 结束时间
        self.step = step  # 预报步长
        self.filepath = rldas_path  # rldas 文件路径 这里需要改下
        self.extent = extent       # 出图的范围

        self.forecast_time_list = self.__get_forecast_time_list__()  #获取时间序列

    def __get_forecast_time_list__(self):
        """
        这里规定,如果间隔时常为24小时的话，开始时间到结束时间不足
        :return:
        """
        time_length = self.end_time - self.start_time
        days = time_length.days
        seconds = time_length.seconds
        hours = days * 24 + seconds / 3600  # 计算预报总时长
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

    def find_file(self,forecast_time:datetime.datetime,attribute:str):
        """
        :descript: 从单个预报时间来获取文件
        :return:
        """
        if attribute=="RAINC":
            # 如果输入的变量为降水,则获取的文件为 前一时刻的降水量
            pre_forecast_time_str=forecast_time+datetime.timedelta(hours=-self.step)


        else:
            #新建一个列表,里面存储检索到的文件
            file_list = []
            for i in range(self.step):
                # 暂时先这样吧,以后再改
                temp_time_str = (forecast_time + datetime.timedelta(hours=i + 1)).strftime('%Y%m%d%H')
                file = glob(self.filepath + '\\*-{attr}-{time_str}_*.nc'.format(attr=attribute, time_str=temp_time_str))
                if len(file) > 0:
                    file_list.append(file[0])
                else:
                    print("当前时段:{} 没有数据,可能造成计算错误".format(temp_time_str))
                    continue

        pass

def get_rldas_path_from_time(forecast_time):
    pass

def composite(files,method):
    stack_data_array=np.array([],dtype=np.float32)
    if method=='sum':
        pass
    elif method=='max':
        pass
    elif method=='avg':
        pass
    elif method=='min':
        pass
    else:
        print("输入的合成方式错误!!!!")

