# -*- coding: utf-8 -*-
'''
Date         : 2023-07-27 16:27:51
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-31 19:21:32
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
    def __init__(self, fpath, variable_name,variables,ticks,forecast_path_str,manual_time=None, forecast_step=3, end=75, forecast_type='short-term'):
        '''
        :param fpath: 没搞懂这是啥
        :param variable_name: 变量名称
        :param city_path: 地级市矢量
        :param province_path: 省级矢量
        :param variables: 变量名，这又是啥
        :param ticks: 坐标范围
        :param manual_time: 运行时间
        :param forecast_step: 预报步长
        :param end: 结束时间?
        :param forecast_type:预报类型
        '''
        self.fpath = fpath
        self.variable_name = variable_name
        self.manual_time = manual_time
        self.forecast_step = forecast_step
        self.end = end
        # self.city_path = city_path
        # self.province_path = province_path
        self.variables = variables
        self.forecast_type = forecast_type  #
        self.ticks=ticks
        self.forecast_path_str=forecast_path_str


        #行政区矢量位置

        self.city_path='./share/region/heilongjiang_shp/heilongjiang_city.shp'
        self.province_path='./share/region/heilongjiang_shp/heilongjiang.shp'


        # 河流矢量 path
        self.level1rivers='./share/river/heilongjiang_level1.shp'
        self.level23rivers='./share/river/heilongjiang_level23.shp'
        self.level4rivers='./share/river/heilongjiang_level4.shp'
        self.level5rivers='./share/river/heilongjiang_level5.shp'
        
        
    # todo:  完成文件夹的创建
    def get_output_file_path(self, variable_name, index, output_prefix,file_name):
        # 获取输出文件路径
        variable_folder = variable_name
        #file_name = f'{self.forecast_type}_{str(self.forecast_step)}h_{variable_folder}_{index}.png'
        output_path = os.path.join(output_prefix, self.forecast_type,self.forecast_path_str, variable_folder, file_name)
        #output_path=output_path.encode("utf-8").decode('utf-8')
        #output_path.decode('gbk').encode('utf-8')
        #print(output_path)
        return output_path

    def create_subdirectories(self, base_path):
        # 创建子文件夹
        path_dict = dict()
        for variable in self.variables:
            # 将变量名中的空格转换为下划线
            # 按照预报类型创建文件夹:短期，中期，短临
            # 
            variable_folder = variable.replace(' ', '_')
            subdirectory = os.path.join(base_path,self.forecast_type,self.forecast_path_str, variable_folder)
            path_dict[variable] = subdirectory
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory)
        return path_dict

    def add_river_shp(self,ax):
        # 这里更改为 一个函数,将河流矢量添加到图像中
        river_level1=cfeature.ShapelyFeature(Reader(self.level1rivers).geometries(), ccrs.PlateCarree(), edgecolor='r',
                                facecolor='none',linewidth=1.0)
        river_level23=cfeature.ShapelyFeature(Reader(self.level23rivers).geometries(), ccrs.PlateCarree(), edgecolor='r',
                                facecolor='none',linewidth=0.8)
        river_level4=cfeature.ShapelyFeature(Reader(self.level4rivers).geometries(), ccrs.PlateCarree(), edgecolor='b',
                                facecolor='none',linewidth=0.5)
        river_level5=cfeature.ShapelyFeature(Reader(self.level5rivers).geometries(), ccrs.PlateCarree(), edgecolor='b',
                                facecolor='none',linewidth=0.5)
        print("已将矢量添加到绘图程序")

        # 将河流水系添加到地图中
        ax.add_feature(river_level1) #添加一级河流
        ax.add_feature(river_level23) #添加二三级河流
        ax.add_feature(river_level4)  #添加四级河流
        ax.add_feature(river_level5) #添加五级河流

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

    def plot_contour_map (self, lat, lon, data, variable_label, levels, colormap, title, output_file, tips='colors',draw_river=False):
        fig = plt.figure (figsize=(8, 8), dpi=400)
        ax = fig.add_axes ([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree ())

        #添加地图要素:行政区和行政区名称
        self.add_map_features (ax)
        if tips == 'colors':
            a = ax.contourf (lon, lat, data, levels=levels, colors=colormap)#,extend='max')
        elif tips == 'cmaps':
            a = ax.contourf (lon, lat, data, levels=levels, cmap=colormap)#,extend='max')

        province = cfeature.ShapelyFeature (Reader (self.province_path).geometries (), ccrs.PlateCarree (), edgecolor='k', facecolor='none')
        ax.add_feature (province)

        #添加河流
        if draw_river==True:
            self.add_river_shp(ax)
        else:
            pass

        #边缘裁剪，白化
        records = Reader (self.province_path).records ()
        for record in records:
            path = Path.make_compound_path (*geos_to_path ([record.geometry]))

        for collection in a.collections:
            collection.set_clip_path (path, transform=ax.transData)

        plt.title (title, fontsize=20, y=1.0)

        cax = fig.add_axes ([ax.get_position ().x1 + 0.01, ax.get_position ().y0, 0.02, ax.get_position ().height])
        cb= plt.colorbar (a, cax, label=variable_label)
        
        if self.ticks!=None:
            cb.set_ticks(self.ticks)
        else:
            pass

        cb.update_ticks()
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2,transparent = False,format='png')
        
        #plt.close()
        #plt.show()
        plt.close()
