# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 8:17

@author: lixiang
"""
import os.path

#%%
import numpy as np
import re
from glob import glob
import datetime
from netCDF4 import Dataset
from un_config.rldas_configl import rldas_path,extent
from wrf import (get_cartopy, latlon_coords, to_np, cartopy_xlim, cartopy_ylim,
                 getvar, ALL_TIMES)

#%%

"""
RLDAS 模式数据读取,这里先改写一下:读取要素时初始化类还是直接从函数里获取????
"""
class RlDas_Reader(object):
    def __init__(self, start_time, end_time, step,attribute):
        # 开始时间
        self.start_time = start_time
        self.end_time = end_time  # 结束时间
        self.step = step  # 预报步长
        self.filepath = rldas_path  # rldas 文件路径 这里需要改下
        self.extent = extent       # 出图的范围
        self.attribute=attribute   #出图的数据

        self.forecast_time_list = self.__get_forecast_time_list__()  #获取时间序列
        self.__get__wrf_files_info()

    def __get__wrf_files_info(self):
        #这里的时间需要再改一下，如果预报时间不是当前文件夹内部的时间,则去遍历子文件夹下面的子文件夹.
        hours=self.start_time
        if hours>12:
            subpath='wrfoutput-ldas-2km-2nests'
            full_path=os.path.join(self.filepath,subpath)
        elif hours<12:
            subpath='wrfoutput-ldas-2km-2nests-00h'
            full_path=os.path.join(self.filepath,subpath)
        else:
            print("时间错误")
        self.all_files=glob(full_path+'/wrf_out_d02_*')

    def __get_forecast_time_list__(self):
        """
        这里规定,如果间隔时常为24小时的话，开始时间到结束时间不足
        :return:
        """
        time_length = self.end_time - self.start_time
        days = time_length.days
        if days > 4:
            print("RLDAS 产品最长预报天数为4天,当前已超过最长预报天数!!!!")
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
            forecast_start_time_str = forecast_time.strftime("%Y-%m-%d_%H")
            forecast_end_time_str = (forecast_time+datetime.timedelta(hours=self.step)).strftime("%Y-%m-%d_%H")

            start_file=[x for x in self.all_files if re.search(forecast_start_time_str,x)][0]
            end_file=[x for x in self.all_files if re.search((forecast_end_time_str,x))][0]

            return [start_file,end_file]
        else:
            #新建一个列表,里面存储检索到的文件
            file_list = []
            for i in range(self.step):
                # 暂时先这样吧,以后再改
                temp_time_str = (forecast_time + datetime.timedelta(hours=i + 1)).strftime('%Y%m%d%H')
                file =[x for x in self.all_files if re.search(temp_time_str,x)][0]
                if len(file) > 0:
                    file_list.append(file)
                else:
                    print("当前时段:{} 没有数据,可能造成计算错误".format(temp_time_str))
                    continue
            return file_list
    def get_data(self):
        """
        获取数据
        :return:
        """
        data_list=[]
        for forecast_start_time in self.forecast_time_list:
            data_dict = dict()







#从多个文件里合成数据
def composite_other_var(files,attribute,method):
    """
    :param files: 不管时间，只负责合成数据
    :param attribute: 属性
    :param method: 合成方法
    :return: 返回一个数组序列
    """
    stack_array = np.array([], dtype=np.float32)
    for file in files:
        ds = Dataset(file)
        data_array = getvar(ds,attribute,timeidx=ALL_TIMES).values
        if len(stack_array) == 0:
            stack_array = data_array
        else:
            stack_array = np.dstack((stack_array, data_array))
    if method == 'max':
        result_array = np.nanmax(stack_array, axis=2)
        return result_array
    elif method == 'sum':
        result_array = np.sum(stack_array, axis=2)
        return result_array
    elif method == 'avg':
        result_array = np.nanmean(stack_array, axis=2)
        return result_array
    else:
        print("输入的合成方式错误!!!!")


#从两个时刻的文件里获取降水量
def diff_pre(start_rain_file,end_rain_file):
    #读取开始时刻的文件
    start_ds = Dataset(start_rain_file)
    end_ds = Dataset(end_rain_file)

    # 获取前一时刻的降水量
    start_rainc=getvar(start_ds,'RAINC',timeidx=ALL_TIMES)
    start_rainnc=getvar(start_ds,'RAINNC',timeidx=ALL_TIMES)

    start_tot_rain=start_rainc.values+start_rainnc.values

    # 获取后一时刻的降水量
    end_rainc=getvar(end_ds,'RAINC',timeidx=ALL_TIMES)
    end_rainnc=getvar(end_ds,'RAINNC',timeidx=ALL_TIMES)
    end_tot_rain=end_rainc.values+end_rainnc.values
    #做差
    pre=end_tot_rain-start_tot_rain

    return pre












