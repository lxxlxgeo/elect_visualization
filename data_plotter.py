'''
Date         : 2023-07-27 16:27:51
LastEditors  : ChenKt
LastEditTime : 2023-07-28 16:14:14
FilePath     : /elect_visualization/data_plotter.py
Aim          :
Mission      :
'''
#%%
latS = 42.0
latN = 55.0
lonL = 120.0
lonR = 135.5

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.path import Path
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import numpy as np
import geopandas as gpd
import os
from cartopy.mpl.patch import geos_to_path
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False
#%%
class Plotter:
    def __init__(self, fpath, variable_name,city_path, province_path,variables,  manual_time=None, forecast_step=3, end=75, forecast_type='short-term'):
        self.fpath = fpath
        self.variable_name = variable_name
        self.manual_time = manual_time
        self.forecast_step = forecast_step
        self.end = end
        self.city_path = city_path
        self.province_path = province_path
        self.variables = variables
        self.forecast_type = forecast_type  #
    def get_output_file_path(self, variable_name, index, output_prefix):
        # 获取输出文件路径
        variable_folder = variable_name.replace(' ', '_')
        file_name = f'{self.forecast_type}_{str(self.forecast_step)}h_{variable_folder}_{index}.png'
        output_path = os.path.join(output_prefix, self.forecast_type, variable_folder, file_name)
        return output_path

    def create_subdirectories(self, base_path):
        # 创建子文件夹
        path_dict = dict()
        for variable in self.variables:
            # 将变量名中的空格转换为下划线
            variable_folder = variable.replace(' ', '_')
            subdirectory = os.path.join(base_path, self.forecast_type, variable_folder)
            path_dict[variable] = subdirectory
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory)
        return path_dict

    # @staticmethod
    def add_map_features (self,ax):
        city_name = gpd.read_file (self.city_path, encoding='utf-8')
        for x, y, label in zip (city_name.representative_point ().x, city_name.representative_point ().y, city_name ['地名']):
            ax.text (x - 0.1, y, label, fontsize=10)

        ax.add_geometries (city_name.geometry, ccrs.PlateCarree (),
                          edgecolor='k', facecolor='none', linewidth=0.5)

        ax.set_xticks (np.arange (lonL, lonR, 2.0), crs=ccrs.PlateCarree ())
        ax.set_yticks (np.arange (latS, latN, 2.0), crs=ccrs.PlateCarree ())

        lon_formatter = LongitudeFormatter (zero_direction_label=False)
        lat_formatter = LatitudeFormatter ()
        ax.xaxis.set_major_formatter (lon_formatter)
        ax.yaxis.set_major_formatter (lat_formatter)

    def plot_contour_map (self, lat, lon, data, variable_label, levels, colormap, title, output_file, tips='colors'):
        fig = plt.figure (figsize=(8, 8), dpi=400)
        ax = fig.add_axes ([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree ())

        self.add_map_features (ax)
        if tips == 'colors':
            a = ax.contourf (lon, lat, data, levels=levels, colors=colormap,extend='max')
        elif tips == 'cmaps':
            a = ax.contourf (lon, lat, data, levels=levels, cmap=colormap,extend='max')

        province = cfeature.ShapelyFeature (Reader (self.province_path).geometries (), ccrs.PlateCarree (), edgecolor='k', facecolor='none')
        ax.add_feature (province)

        records = Reader (self.province_path).records ()
        for record in records:
            path = Path.make_compound_path (*geos_to_path ([record.geometry]))

        for collection in a.collections:
            collection.set_clip_path (path, transform=ax.transData)

        plt.title (title, fontsize=20, y=1.0)

        cax = fig.add_axes ([ax.get_position ().x1 + 0.01, ax.get_position ().y0, 0.02, ax.get_position ().height])
        cb = plt.colorbar (a, cax, label=variable_label)
        cb.update_ticks ()

        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2)
        plt.close()
        # plt.show()
