'''
Date         : 2023-07-24 15:29:57
LastEditors  : ChenKt
LastEditTime : 2023-07-24 17:03:42
FilePath     : /2023项目-黑龙江电科院-微气象服务/EC_D1D_PLOT_auto/plot_ecmwf_cape_tp_windspeed.py
Aim          :
Mission      :
'''
# plot_3h.py
import os
import glob
import cmaps
import numpy as np
from utils import Plotter
import datetime
out_dir = 'G:\js_elect\ECFile\outpng'
current_time = datetime.datetime.now()
two_hour = datetime.timedelta(hours=2)
two_hour_later = current_time + two_hour
formatted_time = two_hour_later.strftime('%Y%m%d%H')

LAT_S = 44.0
LAT_N = 50.0
LON_W = 124.0
LON_E = 134.5

# %%


def main():
    lat_range = (LAT_S, LAT_N)
    lon_range = (LON_W, LON_E)
    # data_files = sorted(glob.iglob('E:/EC/2023072300_grib/*.grib1'))
    # 获取当前系统时间

    # 构建更新后的文件路径
    file_path = "G:/js_elect/ECFile/decode/2023072312/sfc*.grib1"
    # 使用glob模块获取匹配的文件列表
    data_files = sorted(glob.glob(file_path))

    plotter = Plotter()

    for i in range(0, len(data_files) - 1):
        # Read and plot rainfall map (3-hour)
        data_rainfall_3h = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, 'tp', i, 1)
        step = data_rainfall_3h[4]
        base_output_path = os.path.join(out_dir, 'heilongjiang_output')
        #base_output_path = out_dir+'heilongjiang_output'

        output_file_rainfall_3h = plotter.create_subdirectories(
            base_output_path)['tp']+"/heilongjiang_"+formatted_time+"_3hour_rainfall.png"
        plotter.plot_contour_map(data_rainfall_3h, '降水量/$mm$', [0, 0.1, 10, 25, 50, 100, 250, 500],
                                 ['#FFFFFF', '#A6F28F', '#3DBA3D', '#61BBFF',
                                     '#0000FF', '#FA00FA', '#800040'],
                                 '松花江流域降水量预报图 (3-hour)', output_file_rainfall_3h, tips='colors')

        # plotter.plot_contour_map(data_rainfall_3h, '降水量/$mm$', [0, 0.1, 10, 25, 50, 100, 250, 500],
        #                          ['#FFFFFF', '#A6F28F', '#3DBA3D', '#61BBFF',
        #                              '#0000FF', '#FA00FA', '#800040'],
        #                          '黑龙江降水量预报图 (3-hour)', output_file_rainfall_3h, tips='colors')

        # Read and plot rainfall map (3-hour)
        data_rainfall_24h = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, "tp", i, 7)
        step = data_rainfall_24h[4]
        #base_output_path = 'E:/EC/heilongjiang_output'

        output_file_rainfall_24h = plotter.create_subdirectories(
            base_output_path)['tp']+"/heilongjiang_"+formatted_time+"_24hour_rainfall.png"
        plotter.plot_contour_map(data_rainfall_24h, '降水量/$mm$', [0, 0.1, 10, 25, 50, 100, 250, 500],
                                 ['#FFFFFF', '#A6F28F', '#3DBA3D', '#61BBFF',
                                     '#0000FF', '#FA00FA', '#800040'],
                                 '松花江流域降水量预报图 (24-hour)', output_file_rainfall_24h, tips='colors')

        # Read and plot CAPE map (3-hour)
        data_cape = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, "cape", i, 1)
        step = data_cape[4]
        output_file_cape_3h = plotter.create_subdirectories(
            base_output_path)['cape']+formatted_time+"_3hour_cape.png"
        plotter.plot_contour_map(data_cape, '对流有效位能/$J/kg$', np.arange(200, 3001, 200), cmaps.WhBlGrYeRe,
                                 '松花江流域对流有效位能预报图 (3-hour)', output_file_cape_3h, tips='cmaps')

        # data_cape = plotter.read_grib_dataset(
        #     data_files, lat_range, lon_range, "cape", i, 1)
        # step = data_cape[4]
        # output_file_cape_3h = plotter.create_subdirectories(
        #     base_output_path)['cape']+formatted_time+"_3hour_cape.png"
        # plotter.plot_contour_map(data_cape, '对流有效位能/$J/kg$', np.arange(200, 3001, 200), cmaps.WhBlGrYeRe,
        #                          '黑龙江对流有效位能预报图 (3-hour)', output_file_cape_3h, tips='cmaps')

        # Read and plot wind speed map (3-hour)
        # data_wind_3h = plotter.read_grib_dataset(
        #     data_files, lat_range, lon_range, "fg310", i, 1)
        # step = data_wind_3h[4]
        # output_file_wind_3h = plotter.create_subdirectories(
        #     base_output_path)['fg310'] + \
        #     formatted_time+"_3hour_windspeed.png"
        # plotter.plot_contour_map(data_wind_3h, '风速/$m/s$', np.arange(0, 35, 2), cmaps.wind_17lev,
        #                          '黑龙江最大风速预报图 (3-hour)', output_file_wind_3h, tips='cmaps')
        data_wind_3h = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, "fg310", i, 1)
        step = data_wind_3h[4]
        output_file_wind_3h = plotter.create_subdirectories(
            base_output_path)['fg310'] + \
            formatted_time+"_3hour_windspeed.png"
        plotter.plot_contour_map(data_wind_3h, '风速/$m/s$', np.arange(0, 35, 2), cmaps.wind_17lev,
                                 '松花江流域最大风速预报图 (3-hour)', output_file_wind_3h, tips='cmaps')

    for j in range(0, len(data_files) + 1, 2):
        # Read and plot rainfall map (6-hour)
        data_rainfall_6h = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, "tp", j, 2)
        step = data_rainfall_6h[4]
        output_file_rainfall_6h = plotter.create_subdirectories(
            base_output_path)['tp'] + \
            formatted_time+"_6hour_rainfall.png"
        plotter.plot_contour_map(data_rainfall_6h, '降水量/$mm$', [0, 0.1, 10, 25, 50, 100, 250, 500],
                                 ['#FFFFFF', '#A6F28F', '#3DBA3D', '#61BBFF',
                                     '#0000FF', '#FA00FA', '#800040'],
                                 '黑龙江降水量预报图 (6-hour)', output_file_rainfall_6h, tips='colors')

        # Read and plot wind speed map (6-hour)
        data_wind_6h = plotter.read_grib_dataset(
            data_files, lat_range, lon_range, "fg310", j, 2)
        step = data_wind_6h[4]
        output_file_wind_6h = plotter.create_subdirectories(
            base_output_path)['fg310'] + \
            formatted_time+"_6hour_windspeed.png"
        plotter.plot_contour_map(data_wind_6h, '风速/$m/s$', np.arange(0, 35, 2), cmaps.wind_17lev,
                                 '黑龙江最大风速预报图 (6-hour)', output_file_wind_6h, tips='cmaps')


if __name__ == "__main__":
    main()
