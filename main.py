"""
Date         : 2023-07-26 16:13:18
LastEditors  : ChenKt
LastEditTime : 2023-07-28 16:25:04
FilePath     : /elect_visualization/main.py
Aim          :
Mission      :
"""
# %%
import datetime
from data_reader import GribDataReader
from data_plotter import Plotter
import numpy as np
import cmaps
import os

# %%

# %%
fpath = "/mnt/d/kt/project/yl/2023-HLJIEE-MicroMeteorologicalServices/ECMWF/C1D-grib/"
# 数据路径
latS = 42.0
latN = 55.0
lonL = 120.0
lonR = 135.5

variable_name = [
    "Convective available potential energy",
    "Total precipitation",
    "10 metre wind gust in the last 3 hours",
    #  '10 metre wind gust in the last 6 hours'
]
# 变量名，用于提取数据
variable_name_Zh = ["对流有效位能", "降水量", "最大风速"]
# 变量中文名用于生成图片中的标题
city_path = "./old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp"
province_path = "./old/EC_D1D_PLOT/heilongjiang_shp/"
manual_time = datetime.datetime(2023, 7, 25, 17)  # 手动运行时指定的起报时刻（utc-8）
forecast_step = 3
end = 42
forecast_type = "short-term"  # Set the forecast type to 'short-term', 'medium-term', or 'long-term'
output_prefix = "../output/"  # 输出图片路径前缀，命名
# %%
cape_reader = GribDataReader(
    fpath, variable_name[0], manual_time=manual_time, forecast_step=forecast_step, end=end
)
cape, lats, lons = cape_reader.get_data()
forecast_start_time = cape_reader.base_time_str
forecast_end_time = cape_reader.forecast_time_str
# %%
tp_reader = GribDataReader(
    fpath, variable_name[1], manual_time=manual_time, forecast_step=forecast_step, end=end
)
tp, _, _ = tp_reader.get_data()

windspeed_reader = GribDataReader(
    fpath, variable_name[2], manual_time=manual_time, forecast_step=forecast_step, end=end
)
windspeed, _, _ = windspeed_reader.get_data()


# %%

# %%

for i in range(0, len(cape) - 1):
    levels = [0, 0.1, 1, 3, 10, 20, 50, 70]
    plotter = Plotter(        fpath,
        variable_name[0],
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[0]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[0].replace(" ", "_")}_{i}.png'
    output_file = plotter.get_output_file_path(variable_name[0], i, output_prefix)
    subdirectories = plotter.create_subdirectories(output_prefix)
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
    plotter.plot_contour_map(
        lats,
        lons,
        cape[i],
        "对流有效位能/$J/kg$",
        levels=np.arange(200, 3001, 200),
        colormap=cmaps.WhBlGrYeRe,
        title=titles,
        output_file=output_file,
        tips="cmaps",
    )
    del titles, output_file
    plotter = Plotter(
        fpath,
        variable_name[1],
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )
    levels = [0, 0.1, 1, 3, 10, 20, 50, 70]
    color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[1]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[1].replace(" ", "_")}_{i}.png'
    output_file = plotter.get_output_file_path(variable_name[1], i, output_prefix)
    subdirectories = plotter.create_subdirectories(output_prefix)
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
    plotter.plot_contour_map(
        lats,
        lons,
        tp[i],
        "降水量/$mm$",
        levels=levels,
        colormap=color,
        title=titles,
        output_file=output_file,
        tips="colors",
    )
    del titles, output_file

    plotter = Plotter(
        fpath,
        variable_name[2],
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[2]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[2].replace(" ", "_")}_{i}.png'
    output_file = plotter.get_output_file_path(variable_name[2], i, output_prefix)
    subdirectories = plotter.create_subdirectories(output_prefix)
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
    plotter.plot_contour_map(
        lats,
        lons,
        tp[i],
        "风速/$m/s$",
        levels=np.arange(0, 35, 2),
        colormap=cmaps.wind_17lev,
        #  colormap=color,
        title=titles,
        output_file=output_file,
        tips="cmaps",
    )
    del titles, output_file

# %%
