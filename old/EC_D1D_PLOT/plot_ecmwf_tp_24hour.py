# -*- coding: utf-8 -*-
# @Time    : 2022/3/31 19:27
# @Author  : Peipei Liu
# @Email   : liuppei@126.com
# @File    : plot_cmpa_rainfall.py


import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.path import Path
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import numpy as np
from cartopy.mpl.patch import geos_to_path
import geopandas as gpd
import glob
plt.rcParams['font.sans-serif'] = ['SimHei']


latS = 42.0
latN = 55.0
lonW = 120.0
lonE = 135.5
data_file = glob.glob(r'G:\js_elect\ECFile\decode\2023072312\sfc*.grib1')
print(data_file)
for i in range(len(data_file)):
    data1 = xr.open_dataset(data_file[i], engine='cfgrib')
    data2 = xr.open_dataset(data_file[i+7], engine='cfgrib')

    lon = data1['longitude'].loc[lonW:lonE]  # 读取经度
    lat = data1['latitude'].loc[latN:latS]  # 读取纬度
# print(lat)
    pre1 = data1["tp"][:, :].sel(latitude=slice(
        latN, latS), longitude=slice(lonW, lonE))*1000
    pre2 = data2["tp"][:, :].sel(latitude=slice(
        latN, latS), longitude=slice(lonW, lonE))*1000
    pre = pre2-pre1
# print(pre)
    time = data2['time'].data
    step = data2['step'].data/360
    valid_time = data2['valid_time'].data
    print(time)
    print(step)
    print(valid_time)

    fig = plt.figure(figsize=(8, 8), dpi=400)
    proj = ccrs.PlateCarree()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=proj)

    province_path = 'E:/workproject/elect_visualization/old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang.shp'
    province = Reader(province_path)
    city = "E:/workproject/elect_visualization/old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp"
    city_name = gpd.read_file(city, encoding='utf-8')
    # print(city_name)
    for x, y, label in zip(city_name.representative_point().x, city_name.representative_point().y, city_name['地名']):
        ax.text(x-0.1, y, label, fontsize=10)
    city_feature = cfeature.ShapelyFeature(
        Reader(city).geometries(), proj, edgecolor='k', facecolor='none')
    province_feature = cfeature.ShapelyFeature(
        Reader(province_path).geometries(), proj, edgecolor='k', facecolor='none')
    ax.set_extent([lonW, lonE, latS, latN], crs=proj)
    ax.add_feature(province_feature)
    ax.add_feature(city_feature, linewidth=0.5, edgecolor='black')
    ax.set_xticks(np.arange(lonW, lonE, 2.0), crs=proj)
    ax.set_yticks(np.arange(latS, latN, 2.0), crs=proj)
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.tick_params(axis='both', labelsize=12, direction='out')
    color = ('#FFFFFF', '#A6F28F', '#3DBA3D',
             '#61BBFF', '#0000FF', '#FA00FA', '#800040')
    # lonP,latP = np.meshgrid(lon,lat)
    a = ax.contourf(lon, lat, pre, levels=[
                    0, 0.1, 10, 25, 50, 100, 250, 500], colors=color)
    # a = ax.contourf(lon, lat, pre, levels=[0, 0.1, 1, 3, 10, 20, 50, 70], colors=color)
    ######获取path#######################
    records = province.records()
    for record in records:
        path = Path.make_compound_path(*geos_to_path([record.geometry]))
    #######白化###########################
    for collection in a.collections:
        collection.set_clip_path(path, transform=ax.transData)
    plt.title('黑龙江降水量预报图', fontsize=20, y=1.0)
    # plt.text(133.0, 54.3, str(time)[2:13], fontsize=12)
    cax = fig.add_axes([ax.get_position().x1+0.01,
                       ax.get_position().y0, 0.02, ax.get_position().height])
    cb = plt.colorbar(a, cax, label='降水量/$mm$')
    cb.set_ticks([0.1, 10, 25, 50, 100, 250])
    cb.update_ticks()
    plt.savefig(r"G:\js_elect\ECFile\outpng\heilongjiang_output_2023072308_" +
                str(step)[0:2]+"_24hour_pre.png", bbox_inches='tight', pad_inches=0.2)
