'''
Date         : 2023-07-24 15:29:28
LastEditors  : ChenKt
LastEditTime : 2023-07-25 14:03:16
FilePath     : \2023项目-黑龙江电科院-微气象服务\code\EC_D1D_PLOT_auto\utils.py
Aim          :
Mission      :
'''
# utils.py
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

LAT_S = 42.0
LAT_N = 55.0
LON_W = 120.0
LON_E = 135.5

plt.rcParams['font.sans-serif'] = ['SimHei']

class Plotter:
    def __init__(self):
        pass
    def create_subdirectories(self, base_path):
        # 创建子文件夹
        for variable in self.variables:
            subdirectory = os.path.join(base_path, variable)
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory)
    @staticmethod
    # def read_grib_dataset(file_path, lat_range, lon_range, variable_name):
    #     data = xr.open_dataset(file_path, engine='cfgrib')
    #     lat = data['latitude'].loc[lat_range]
    #     lon = data['longitude'].loc[lon_range]
    #     variable_data = data[variable_name][:, :].sel(latitude=slice(lat_range[1], lat_range[0]), longitude=slice(lon_range[0], lon_range[1]))
    #     time = data['time'].data
    #     step = data['step'].data / 360
    #     valid_time = data['valid_time'].data
    #     return lat, lon, variable_data, time, step, valid_time

    def read_grib_dataset(file_path, lat_range, lon_range, variable_name, i,input_step):
        data = xr.open_dataset(file_path, engine='cfgrib')
        lat = data['latitude'].loc[LAT_S:LAT_N]
        lon = data['longitude'].loc[LON_W:LON_E]

        if variable_name == 'tp':
            data1 = xr.open_dataset(file_path[i], engine='cfgrib')
            data2 = xr.open_dataset(file_path[i+input_step], engine='cfgrib')
            variable_data1 = data1[variable_name][:, :].sel(latitude=slice(lat_range[1], lat_range[0]), longitude=slice(lon_range[0], lon_range[1])) * 1000
            variable_data2 = data2[variable_name][:, :].sel(latitude=slice(lat_range[1], lat_range[0]), longitude=slice(lon_range[0], lon_range[1])) * 1000
            variable_data = variable_data2 - variable_data1
        else:
            variable_data = data[variable_name][:, :].sel(latitude=slice(lat_range[1], lat_range[0]), longitude=slice(lon_range[0], lon_range[1]))

        time = data['time'].data
        step = data['step'].data / 360
        valid_time = data['valid_time'].data
        return lat, lon, variable_data, time, step, valid_time
    @staticmethod
    def add_map_features(ax):
        province_path = r'E:/EC/heilongjiang_shp/heilongjiang.shp'
        province = cfeature.ShapelyFeature(Reader(province_path).geometries(), ccrs.PlateCarree(), edgecolor='k', facecolor='none')
        ax.add_feature(province)

        records = province.records()
        for record in records:
            path = Path.make_compound_path(*geos_to_path([record.geometry]))

        for collection in a.collections:
            collection.set_clip_path(path, transform=ax.transData)

        city_path = r"E:/EC/heilongjiang_shp/heilongjiang_city.shp"
        city_name = gpd.read_file(city_path, encoding='utf-8')
        ax.add_geometries(city_name.geometry, ccrs.PlateCarree(), edgecolor='k', facecolor='none', linewidth=0.5)

        ax.set_xticks(np.arange(LON_W, LON_E, 2.0), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(LAT_S, LAT_N, 2.0), crs=ccrs.PlateCarree())

        lon_formatter = LongitudeFormatter(zero_direction_label=False)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)

    @staticmethod
    def plot_contour_map(data, variable_label, levels, colormap, title, output_file):
        lon, lat, variable_data, _, _, _ = data

        fig = plt.figure(figsize=(8, 8), dpi=400)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree())

        Plotter.add_map_features(ax)

        a = ax.contourf(lon, lat, variable_data, levels=levels, cmap=colormap)

        plt.title(title, fontsize=20, y=1.0)

        cax = fig.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02, ax.get_position().height])
        cb = plt.colorbar(a, cax, label=variable_label)
        cb.update_ticks()

        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2)
        plt.close()