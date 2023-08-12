# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 8:17

@author: lixiang
"""

import numpy as np
import re
from glob import glob
import datetime
import xarray as xr


class RlDas_Reader(object):
    def __init__(self,start_time,end_time,step):
        #开始时间
        self.start_time=start_time
        self.end_time=end_time #结束时间
        self.step=step         #预报步长

        pass

    def __get_path_info__(self):
        """
        这里规定,如果间隔时常为24小时的话，开始时间到结束时间不足
        :return:
        """
        # time_length=self.end_time-self.start_time
        time_length = self.end_time - self.start_time
        days = time_length.days
        seconds = time_length.seconds
        hours = days * 24 + seconds / 3600  #计算预报总时长

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

    def __get_files_from_time_(self):
  
        pass

