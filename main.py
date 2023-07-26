'''
Date         : 2023-07-26 16:13:18
LastEditors  : ChenKt
LastEditTime : 2023-07-26 20:00:41
FilePath     : /elect_visualization/main.py
Aim          :
Mission      :
'''
#%%
import xarray as xr
import datetime
import glob
import re
#%%
data_file = glob.glob('../ECMWF/C1D-grib/')
current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

date_str = re.findall('\d{8}', f[0])[0]
date_obj = datetime.strptime(date_str, '%y%m%d')
#%%
import os
import datetime
import xarray as xr
import numpy as np

LAT_S = 44.0
LAT_N = 50.0
LON_W = 124.0
LON_E = 134.5


def get_forecast_steps(hour):
    if hour == 11 or hour == 23:
        return list(range(0, 33, 3))
    elif hour == 17 or hour == 5:
        return list(range(0, 33, 3))
        return None

def get_base_time(current_time, forecast_hour):
    if forecast_hour == 11 or forecast_hour == 17:
        base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 0)
    elif forecast_hour == 5 or forecast_hour == 23:
        base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 12)
    else:
        return None
    return base_time

def get_file_names(fpath,base_time, forecast_steps):
    file_names = []
    forecast_time0 = base_time + datetime.timedelta(hours=forecast_steps[0])
    folder_name = forecast_time0.strftime("%Y%m%d%H")
    # forecast_steps = np.arange(0,169,3)
    file_name1 = f"sfc_{forecast_time0.strftime('%Y%m%d')}"
    for step in forecast_steps:
        forecast_time = base_time + datetime.timedelta(hours=step)

        file_name2 = f"_{step}.grib1"
        file_name = file_name1+file_name2
        file_path = os.path.join(fpath,folder_name, file_name)
        file_names.append(file_path)
    return file_names

def read_files(fpath,variable_name,manual_time=None):
    # 获取当前的东八区时间
    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

    # 判断是否使用手动指定的时间
    if manual_time:
        current_time = manual_time

    # 获取当前时间的小时数
    forecast_hour = current_time.hour

    # 获取对应小时数的预报步长
    forecast_steps = get_forecast_steps(forecast_hour)
    if forecast_steps is None:
        print("当前时间不在预定时间范围内（5点，11点，17点，23点）。")
        return

    # 获取基准时间
    base_time = get_base_time(current_time, forecast_hour)
    if base_time is None:
        print("无效的时间信息。")
        return

    # 获取需要读取的文件名列表
    file_names = get_file_names(fpath,base_time, forecast_steps)

    # 读取每个文件的数据

    data = []
    datasets = []
    for file_path in file_names:
        try:
            ds = xr.open_dataset(file_path, engine="cfgrib")
            datasets.append(ds)
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在。")
            continue
    if variable_name == 'tp':
        start_index = 2 if forecast_hour in [5, 17] else 0
    else:
        start_index = 3 if forecast_hour in [5, 17] else 1
    for i in range(start_index, len(file_names)):
        try:
            ds = datasets[i]
            # 根据变量名选择数据
            if variable_name == 'tp':
                if i < len(file_names) - 1:
                    ds_i_plus_1 = ds[i+1].sortby("latitude", ascending=True)
                    ds_i = ds[i].sortby("latitude", ascending=True)
                    ds_i_plus_1 = ds_i_plus_1[variable_name].sel(latitude=slice(LAT_S,LAT_N),longitude=slice(LON_W,LON_E))*1000
                    ds_i = ds[variable_name].sel(latitude=slice(LAT_S,LAT_N),longitude=slice(LON_W,LON_E))*1000
                    ds_diff = ds_i_plus_1 - ds_i
                    data.append(ds_diff)
                else:
                    print(f"文件 {file_path} 是最后一个文件，无法计算差分。")
            else:
                ds_i = ds[variable_name].sel(latitude=slice(LAT_S,LAT_N),longitude=slice(LON_W,LON_E))
                data.append(ds_i)
            print(ds)
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在。")
            continue

    return data

# 调用函数读取数据，不指定时间时使用当前时间
fpath='../ECMWF/C1D-grib/'
# data = read_files(fpath)

# 手动指定时间为2023年7月24日11时
manual_time = datetime.datetime(2023, 7, 25, 11)
data_manual = read_files(fpath,'tp',manual_time=manual_time)
# %%
data_manual[0]['longitude']
# %%
import os
import datetime
import xarray as xr
import numpy as np

LAT_S = 44.0
LAT_N = 50.0
LON_W = 124.0
LON_E = 134.5
variable_name = ['tp', 'cape', 'fg310']
class ReadData:
    def __init__(self):
        pass

    def get_forecast_steps(self, hour):

        if hour in [11, 23]:
            return list(range(0, 7, 3))#短临25
        elif hour in [17, 5]:
            return list(range(0, 7, 3))#
        return None

    def get_base_time(self, current_time, forecast_hour):
        if forecast_hour in [11, 17]:
            base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 0)
        elif forecast_hour in [5, 23]:
            base_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 12)
        else:
            return None
        return base_time

    def get_file_names(self, fpath, base_time, forecast_steps):
        file_names = []
        forecast_time0 = base_time + datetime.timedelta(hours=forecast_steps[0])
        folder_name = forecast_time0.strftime("%Y%m%d%H")
        file_name1 = f"sfc_{forecast_time0.strftime('%Y%m%d')}"
        for step in forecast_steps:
            forecast_time = base_time + datetime.timedelta(hours=step)
            file_name2 = f"_{step}.grib1"
            file_name = file_name1 + file_name2
            file_path = os.path.join(fpath, folder_name, file_name)
            file_names.append(file_path)
        return file_names

    def read_files(self, fpath, variable_name, manual_time=None):
        current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

        if manual_time:
            current_time = manual_time

        forecast_hour = current_time.hour
        forecast_steps = self.get_forecast_steps(forecast_hour)
        if forecast_steps is None:
            print("当前时间不在预定时间范围内（5点，11点，17点，23点）。")
            return

        base_time = self.get_base_time(current_time, forecast_hour)
        if base_time is None:
            print("无效的时间信息。")
            return

        file_names = self.get_file_names(fpath, base_time, forecast_steps)

        data = []
        datasets = []
        for file_path in file_names:
            try:
                ds = xr.open_dataset(file_path, engine="cfgrib")
                datasets.append(ds)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        if variable_name == 'tp':
            start_index = 2 if forecast_hour in [5, 17] else 0
        else:
            start_index = 3 if forecast_hour in [5, 17] else 1

        for i in range(start_index, len(file_names)):
            try:
                ds = datasets[i]
                if variable_name == 'tp':
                    if i < len(file_names) - 1:
                        ds_i_plus_1 = datasets[i + 1]#.sortby("latitude", ascending=True)
                        ds_i = datasets[i]#.sortby("latitude", ascending=True)
                        ds_i_plus_1 = ds_i_plus_1[variable_name].sel(latitude=slice(LAT_N, LAT_S),
                                                                    longitude=slice(LON_W, LON_E)) * 1000
                        ds_i = ds[variable_name].sel(latitude=slice(LAT_N, LAT_S), longitude=slice(LON_W, LON_E)) * 1000
                        ds_diff = ds_i_plus_1 - ds_i
                        data.append(ds_diff)
                    else:
                        print(f"文件 {file_path} 是最后一个文件，无法计算差分。")
                else:
                    ds_i = ds[variable_name].sel(latitude=slice(LAT_N, LAT_S), longitude=slice(LON_W, LON_E))
                    data.append(ds_i)
                print(ds)
            except FileNotFoundError:
                print(f"文件 {file_path} 不存在。")
                continue

        return data
# %%
readData = ReadData()
manual_time = datetime.datetime(2023, 7, 25, 11)
# data_manual = read_files(fpath,'tp',manual_time=manual_time)
data = readData.read_files(fpath='../ECMWF/C1D-grib/', variable_name='',manual_time=manual_time)
# %%
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.path import Path
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import numpy as np
import geopandas as gpd
import glob
import cmaps
import os
import re


from cartopy.mpl.patch import geos_to_path

#plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False
# %%
city_path= './old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp'
province_path='./old/EC_D1D_PLOT/heilongjiang_shp/'
class Plotter:
    def __init__(self):
        self.variables = ['tp', 'cape', 'fg310']
        # pass

    def create_subdirectories(self, base_path):
        # 创建子文件夹
        path_dict = dict()
        for variable in self.variables:
            subdirectory = os.path.join(base_path, variable)
            path_dict[variable] = subdirectory
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory)
        return path_dict
    @staticmethod
    def add_map_features(ax):
        # province_path = 'E:/workproject/elect_visualization/old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp'
        # province = cfeature.ShapelyFeature(Reader(province_path).geometries(), ccrs.PlateCarree(), edgecolor='k', facecolor='none')
        # ax.add_feature(province)

        # records = province.records()
        # for record in records:
        #     path = Path.make_compound_path(*geos_to_path([record.geometry]))

        # for collection in a.collections:
        #     collection.set_clip_path(path, transform=ax.transData)

        # 添加城市名称
        #city_path = "E:/workproject/elect_visualization/old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp"
        city_name = gpd.read_file(city_path, encoding='utf-8')

        #city_name = gpd.read_file(city,encoding='utf-8')
        # print(city_name)
        for x, y, label in zip(city_name.representative_point().x, city_name.representative_point().y, city_name['地名']):
            ax.text(x-0.1, y, label, fontsize=10)

        ax.add_geometries(city_name.geometry, ccrs.PlateCarree(),
                          edgecolor='k', facecolor='none', linewidth=0.5)

        # 添加刻度
        ax.set_xticks(np.arange(LON_W, LON_E, 2.0), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(LAT_S, LAT_N, 2.0), crs=ccrs.PlateCarree())

        # 设置刻度，经纬度字符显示
        lon_formatter = LongitudeFormatter(zero_direction_label=False)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)

    @staticmethod
    def plot_contour_map(data, variable_label, levels, colormap, title, output_file, tips='colors'):
        lon = data['longitude']
        lat = data['latitude']

        fig = plt.figure(figsize=(8, 8), dpi=400)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree())

        Plotter.add_map_features(ax)
        if tips == 'colors':

            a = ax.contourf(lon, lat,data,
                            levels=levels, colors=colormap)
        elif tips == 'cmaps':
            a = ax.contourf(lon, lat,data,
                            levels=levels, cmaps=colormap)

        #province_path = 'E:/workproject/elect_visualization/old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp'
        province = cfeature.ShapelyFeature(Reader(province_path).geometries(
        ), ccrs.PlateCarree(), edgecolor='k', facecolor='none')
        ax.add_feature(province)

        records = Reader(province_path).records()
        for record in records:
            path = Path.make_compound_path(*geos_to_path([record.geometry]))

        for collection in a.collections:
            collection.set_clip_path(path, transform=ax.transData)

        plt.title(title, fontsize=20, y=1.0)

        cax = fig.add_axes([ax.get_position().x1 + 0.01,
                           ax.get_position().y0, 0.02, ax.get_position().height])
        cb = plt.colorbar(a, cax, label=variable_label)
        cb.update_ticks()

        # plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2)
        plt.show()
# %%
for i in range(0, len(data) - 1):
    Plotter.plot_contour_map(data[i], '降水量/$mm$', [0, 0.1, 10, 25, 50, 100, 250, 500],
                                 ['#FFFFFF', '#A6F28F', '#3DBA3D', '#61BBFF',
                                     '#0000FF', '#FA00FA', '#800040'],
                                 '黑龙江降水量预报图 (6-hour)', './output_file_rainfall_6h', tips='colors')
# %%
