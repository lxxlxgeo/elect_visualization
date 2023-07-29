'''
Date         : 2023-07-27 16:26:01
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-29 16:03:30
FilePath     : /elect_visualization/data_reader.py
Aim          : Read grib data and extract required variables along with their corresponding latitude and longitude information, as well as forecast start and end time.
Mission      :
'''
import datetime
import os
import pygrib

# fpath = '/mnt/d/kt/project/yl/2023-HLJIEE-MicroMeteorologicalServices/ECMWF/C1D-grib/'
fpath = '/share/Datasets/ECMWF/C1D-grib'

latS = 42.0
latN = 55.0
lonL = 120.0
lonR = 135.5
variable_name = ['Convective available potential energy',
                 'Total precipitation',
                 '10 metre wind gust in the last 3 hours',
                 '10 metre wind gust in the last 6 hours'
                 ]
variable_name_Zh = ['对流有效位能',
                    '降水量',
                    '最大风速'
                    ]

manual_time = datetime.datetime(2023, 7, 25, 11)
forecast_step = 3
end = 42


class GribDataReader:
    def __init__(self, fpath, variable_name, manual_time=None, forecast_step=3, end=75):
        self.fpath = fpath
        self.variable_name = variable_name
        self.manual_time = manual_time
        self.forecast_step = forecast_step
        self.end = end

    def get_forecast_steps(self, hour):
        if hour == 11 or hour == 23:
            return list(range(0, self.end, self.forecast_step))
        elif hour == 17 or hour == 5:
            # return list(range(9, self.end, self.forecast_step))
            print(list(range(0, self.end, self.forecast_step)))
            return list(range(0, self.end, self.forecast_step))
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
                # ds_i = grbs_list[i].select(name=self.variable_name)[0]

                base_time_str = (base_time + datetime.timedelta(hours=8) + datetime.timedelta(
                    hours=forecast_steps[i])).strftime('%m月%d日%H时')
                forecast_time_str = (base_time + + datetime.timedelta(hours=8) + datetime.timedelta(
                    hours=forecast_steps[i] + self.forecast_step)).strftime('%m月%d日%H时')

                base_times.append(base_time_str)
                forecast_times.append(forecast_time_str)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        return base_times, forecast_times

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
                print(file_path)
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
                        ds_diff = (ds_i_plus_1_values - ds_i_values) * 1000
                        data.append(ds_diff)
                        if lats is None or lons is None:
                            lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
                    else:
                        print(f"文件 {file_path} 是最后一个文件，无法计算差分。")
                else:
                    if i < len(grbs_list) - 1:
                        print(len(grbs_list))
                        print(self.variable_name)

                        ds_i = grbs_list[i + 1].select(name=self.variable_name)[0]
                        # print(grbs_list)
                        ds_i_values = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[0]
                        data.append(ds_i_values)
                        if lats is None or lons is None:
                            lats, lons = ds_i.data(lat1=latS, lat2=latN, lon1=lonL, lon2=lonR)[1:3]
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        # 获取预报起始时刻和预报时刻滞后step个小时的时间字符串列表
        self.base_time_str, self.forecast_time_str = self.get_time_strings(base_time, forecast_steps)
        return data, lats, lons