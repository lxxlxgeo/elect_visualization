# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 20:33:44 2023

@author: my_pc
"""

import re
import os
from glob import glob
import pathlib
import datetime
import xarray as xr


class ReadGribData(object):
    def __init__(self, file):
        self.file = file
        self.basename = os.path.basename(file)
        self.filetime = self.get_time_from_basename()

    def get_time_from_basename(self):
        filebasename = self.basename
        time_day = datetime.datetime.strptime(
            re.findall('\d{8}', filebasename)[0], '%Y%m%d')
        hours = re.findall('_\d+.grib.', filebasename)
        hour_int = int(hours[0].split('.')[0].split('_')[1])
        time_ok = time_day+datetime.timedelta(hours=hour_int)
        return time_ok
        # self.filetime=time_ok

    # 获取前一时刻的降水量数据
    def get_pre_times_file(self, files, d_hour=-3):
        pretime = self.filetime+datetime.timedelta(hours=d_hour)
        front_time_str = pretime.strftime('%Y%m%d_%H')
        front_file = [x for x in files if re.search(front_time_str, x)][0]
        return front_file

    def get_Data(self, extent, attribute):
        ds = xr.open_dataset(self.file, engine='cfgrib')

        pass
