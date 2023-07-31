# -*- coding: utf-8 -*-
import datetime
import os,re
import pygrib
import numpy as np
from .configure import lonL,lonR,latS,latN   #从配置文件py里获取范围

class GribDataReader:
    def __init__(self, fpath, variable_name,forecast_type,forecast_type_tips,manual_time=None, forecast_step=3, end=75,):
        self.fpath = fpath
        self.variable_name = variable_name
        self.forecast_type=forecast_type
        self.forecast_type_tips=forecast_type_tips
        self.manual_time = manual_time
        self.forecast_step = forecast_step
        self.end = end

    def get_forecast_steps(self, hour):
        # UTC 00时数据到达时间为 UTC 8时到
        #UTC 12时的数据为 UTC20 时到
        # 运行时间 05,11,17,23
        # 换算成UTC 为 05 ----> -1天 为前一天的21点运行
        # 11换算成UTC 为 3 点运行
        # 17 换算成UTC 为 09 时运行
        # 23 换算成 UTC 为 15时运行
        #暂定重写此部分
        # if hour==11:
        #     #北京时间11时运行，UTC为03时
        #     return list(range(7,self.end,self.forecast_step))
        # elif hour==5:
        #     return list(range(1,self.end,self.forecast_step))
        # elif hour==17:
        #     return  list(range(9,self.end,self.forecast_step))
        # elif hour==23:
        #     return  list(range(15,self.forecast_step,self.forecast_step))
        if self.forecast_type=='imminent':
            if hour==5:
                return list(1,self.end,self.forecast_step)
            elif hour==11:
                return list(7,self.end,self.forecast_step)
            elif hour==17:
                return list(1,self.end,self.forecast_step)
            elif hour==23:
                return list(7,self.end,self.forecast_step)
        else:
            if hour == 11 or hour == 23:
                return list(range(0, self.end, self.forecast_step))
                print(range(0, self.end, self.forecast_step))
            elif hour == 17 or hour == 5:
                #return list(range(9, self.end, self.forecast_step))
                print(list(range(12, self.end, self.forecast_step)))
                return list(range(12, self.end, self.forecast_step))
        return None

    def get_base_time(self, current_time, forecast_hour):
        if forecast_hour == 11 or forecast_hour == 17:
            base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 0)
        elif forecast_hour == 5 or forecast_hour == 23:
            base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 12)
        else:
            return None
        return base_time

    def get_file_names(self, base_time, forecast_steps):
        file_names = []
        # forecast_time0 = base_time + datetime.timedelta(hours=forecast_steps[0])
        forecast_time0 = base_time
        folder_name = forecast_time0.strftime("%Y%m%d%H")
        file_name1 = f"sfc_{forecast_time0.strftime('%Y%m%d')}"
        for step in forecast_steps:
            forecast_time = base_time + datetime.timedelta(hours=step)
            file_name2 = f"_{str(step)}.grib1"
            file_name = file_name1 + file_name2
            file_path = os.path.join(self.fpath, folder_name, file_name)
            file_names.append(file_path)
        return file_names
    def get_time_strings(self, base_time, forecast_steps):
        base_times = []
        forecast_times = []

        file_names = self.get_file_names(base_time, forecast_steps)
        if not file_names:
            return base_times, forecast_times

        # grbs_list = [pygrib.open(file_path) for file_path in file_names]
        grbs_list = []
        for file_path in file_names:
            try:
                grbs_list.append(pygrib.open(file_path))
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        for i in range(len(file_names)):
            file_path = file_names[i]
            try:
                #ds_i = grbs_list[i].select(name=self.variable_name)[0]

                base_time_str = (base_time+ datetime.timedelta(hours=8) + datetime.timedelta(hours=forecast_steps[i])).strftime('%m月%d日%H时')
                forecast_time_str = (base_time + + datetime.timedelta(hours=8)+datetime.timedelta(hours=forecast_steps[i] + self.forecast_step)).strftime('%m月%d日%H时')

                base_times.append(base_time_str)
                forecast_times.append(forecast_time_str)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        return base_times, forecast_times

    def get_time_str_mdH(self, base_time, forecast_steps):
        base_times = []
        forecast_times = []

        file_names = self.get_file_names(base_time, forecast_steps)
        if not file_names:
            return base_times, forecast_times

        # grbs_list = [pygrib.open(file_path) for file_path in file_names]
        grbs_list = []
        for file_path in file_names:
            try:
                grbs_list.append(pygrib.open(file_path))
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        for i in range(len(file_names)):
            file_path = file_names[i]
            try:
                #ds_i = grbs_list[i].select(name=self.variable_name)[0]

                base_time_str = (base_time+ datetime.timedelta(hours=8) + datetime.timedelta(hours=forecast_steps[i])).strftime('%m%d%H')
                forecast_time_str = (base_time + + datetime.timedelta(hours=8)+datetime.timedelta(hours=forecast_steps[i] + self.forecast_step)).strftime('%m%d%H')

                base_times.append(base_time_str)
                forecast_times.append(forecast_time_str)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        return base_times, forecast_times
    def get_time_str_YmdH(self, base_time, forecast_steps):
        base_times = []
        forecast_times = []

        file_names = self.get_file_names(base_time, forecast_steps)
        if not file_names:
            return base_times, forecast_times

        # grbs_list = [pygrib.open(file_path) for file_path in file_names]
        grbs_list = []
        for file_path in file_names:
            try:
                grbs_list.append(pygrib.open(file_path))
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        for i in range(len(file_names)):
            file_path = file_names[i]
            try:
                #ds_i = grbs_list[i].select(name=self.variable_name)[0]

                base_time_str = (base_time+ datetime.timedelta(hours=8) + datetime.timedelta(hours=forecast_steps[i])).strftime('%Y%m%d%H')
                forecast_time_str = (base_time + + datetime.timedelta(hours=8)+datetime.timedelta(hours=forecast_steps[i] + self.forecast_step)).strftime('%Y%m%d%H')

                base_times.append(base_time_str)
                forecast_times.append(forecast_time_str)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        return (base_time+ datetime.timedelta(hours=8)).strftime('%Y%m%d%H')
    def get_data(self):
        # 获取当前的东八区时间
        current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

        # 判断是否使用手动指定的时间
        if self.manual_time:
            current_time = self.manual_time

        # 获取当前时间的小时数
        forecast_hour = current_time.hour

        # 获取对应小时数的预报步长
        forecast_steps = self.get_forecast_steps(forecast_hour)
        if forecast_steps is None:
            print("当前时间不在预定时间范围内（5点，11点，17点，23点）。")
            return None

        # 获取基准时间
        base_time = self.get_base_time(current_time, forecast_hour)
        if base_time is None:
            print("无效的时间信息。")
            return None

        # 获取需要读取的文件名列表
        file_names = self.get_file_names(base_time, forecast_steps)

        # 读取每个文件的数据
        data = []
        lats, lons = None, None
        # grbs_list = [pygrib.open(file_path) for file_path in file_names]
        grbs_list = []
        for file_path in file_names:
            try:
                grbs_list.append(pygrib.open(file_path))
                print(file_path,' 文件已读取')
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue
        for i in range(len(file_names)):
            file_path = file_names[i]
            try:
                if self.variable_name == 'Total precipitation':
                    if i < len(grbs_list) - 1:
                        ds_i_plus_1 = grbs_list[i + 1].select(name=self.variable_name)[0]
                        ds_i = grbs_list[i].select(name=self.variable_name)[0]
                        # 获取gribmessage对象的值
                        ds_i_plus_1_values = ds_i_plus_1.data(
                            lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
                        ds_i_values = ds_i.data(
                            lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
                        # 进行减法运算
                        ds_diff = (ds_i_plus_1_values - ds_i_values)*1000
                        data.append(ds_diff)
                        if lats is None or lons is None:
                            lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
                    else:
                        print(f"文件 {file_path} 是最后一个文件，无法计算差分。")
                else:

                    if i<len(grbs_list)-1:
                        if self.forecast_type_tips=='imminent':
                            ds_i=grbs_list[i+1].select(name=self.variable_name)[0]
                            s_i_values = ds_i.data (lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
                            data.append(s_i_values)
                            if lats is None or lons is None:
                                lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
                        else:
                            # maximum synthesis
                            current_file=file_names[i+1]
                            filelist=get_all_files_tocalc_avg(current_file)
                            ds_i_values,lats,lons=avg_files(filelist,self.variable_name,lats,lons,latS,latN,lonL,lonR)
                            # ds_i = grbs_list[i + 1].select(name=self.variable_name)[0]
                            # #print(grbs_list)
                            # ds_i_values = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
                            data.append(ds_i_values)
                            # if lats is None or lons is None:
                            #     lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        # 获取预报起始时刻和预报时刻滞后step个小时的时间字符串列表
        self.base_time_str, self.forecast_time_str = self.get_time_strings(base_time, forecast_steps)
        self.base_time_str_mdH,self.forecast_time_str_mdH=self.get_time_str_mdH(base_time,forecast_steps)
        self.base_time_str_YmdH=self.get_time_str_YmdH(base_time,forecast_steps)

        return data, lats, lons
    
    










# 初始场为十二时的初始场，最终要加12时，但是当前仅仅把所有文件都作为0时来使用
def get_time_from_file(file):
    basename=os.path.basename(file)
    filebasename = basename
    time_day = datetime.datetime.strptime(
        re.findall('\d{8}', filebasename)[0], '%Y%m%d')
    hours = re.findall('_\d+.grib.', filebasename)
    hour_int = int(hours[0].split('.')[0].split('_')[1])
    time_ok = time_day+datetime.timedelta(hours=hour_int)
    return time_ok

def get_current_time_file(current_file,d_hour=-6):
    
    #current_dir=os.path.dirname(current_file)
    current_file_time=get_time_from_file(current_file)
    current_time = current_file_time+datetime.timedelta(hours=d_hour)
    
    if d_hour<0:
        duration=current_file_time-current_time
        day=duration.days
        hour=int(duration.seconds / 3600)
        d_hour_cur= day*24+hour
    
    hours = re.findall('_\d+.grib.', os.path.basename(current_file))
    hour_int = int(hours[0].split('.')[0].split('_')[1]) 
    
    count_hours=hour_int-d_hour_cur

    target_file=re.sub('[1-9].grib1|[1-9][0-9].grib1|[1-9][0-9][0-9].grib1',str(count_hours),current_file)+'.grib1'
    #print(target_file +' is '+str(os.path.exists(target_file)))
    return target_file


def get_all_files_tocalc_avg(file):
    
    file_list=[]
    for i in range(1,4):
        d_hour=i*-6
        targetfile=get_current_time_file(file,d_hour=d_hour)
        file_list.append(targetfile)
    #将自身文件加入
    file_list.append(file)
    return file_list
        
        
def avg_files(files,variable_name,lats,lons,latS,latN,lonL,lonR):
    print("变量 {} 合成中".format(variable_name))
    all_array_list=[]
    for file in files:
        ds=pygrib.open(file)
        ds_i=ds.select(name=variable_name)[0]
        ds_i_values = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
        all_array_list.append(ds_i_values)
        if lats is None or lons is None:
            lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
    
    value_array=np.dstack(all_array_list)
    avg_value=np.nanmax(value_array,axis=2)
    return avg_value,lats,lons

        

        
        
    
        
        