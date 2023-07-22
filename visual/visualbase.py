# -*- coding: utf-8 -*-
"""
Created on Thu May 18 17:22:31 2023

@author: lixiang
"""
# %%
import os.path
import io
import matplotlib
from scipy.interpolate import griddata
import pandas as pd
import numpy as np
from osgeo import gdal, osr
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from osgeo import gdal, osr
import cartopy.io.shapereader as shpreader
import copy
from matplotlib import colors
import cmaps
import matplotlib.colors as mcolors


# %%
def normal_plot_scatter_img(extents, data, lon, lat, filename, title, norm, colormap, level):
    '''
    :param extents: 坐标范围
    :param data: 写入的数据,2D
    :param lon:  定义经度格网,2D
    :param lat:  定义纬度格网,2D
    :param filename: 输出png的文件名,str
    :param title: png标题，已删除的参数，可传入''
    :param norm: 最大值，最小值
    :param colormap: 颜色表
    :param level: 分类
    :return:
    '''
    #data = change_lon(data, lon)

    proj = ccrs.PlateCarree()
    # 设置掩膜透明
    my_cmap = copy.copy(plt.cm.get_cmap('gray'))
    my_cmap.set_bad(alpha=0)
    fig = plt.figure(dpi=600)
    ax = fig.add_subplot(111, projection=proj)
    # filepath = r"J:\农业遥感\气象信息火点\shpfile\jiangsu.shp"
    # reader = shpreader.Reader (filepath)
    # geoms = reader.geometries ()
    # ax.add_geometries(geoms, proj, lw=0.5, fc='none')
    plt.axis('off')
    tdata = data.copy()
    tdata[tdata == 0] = np.nan
    alhpa = np.ones(data.shape)
    nanvalue = np.where((np.isnan(data)))

    alhpa[nanvalue] = 0
    # fig.subplots_adjust(left=0, bottom=0, right=1, top=1,hspace=0,wspace=0)

    # im = ax.imshow(data, extent=extents, interpolation='spline36',
    #                alpha=alhpa, cmap=colormap, norm=norm)
    im2 = ax.contourf(lon, lat, data, extent=extents,
                      cmap=colormap, norm=norm, levels=level, extend="both")
    # im2=plt.imshow(tdata,extent=extents,cmap=my_cmap)
    cbar = fig.colorbar(im2, ax=ax)
    cbar.ax.tick_params(labelsize='small')
    # plt.title(title)
    # plt.imshow()
    #plt.savefig(filename, format='png', bbox_inches='tight', dpi=400, pad_inches=0.0,transparent = True)
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=600)
    plt.close()
    del ax, im2, fig
