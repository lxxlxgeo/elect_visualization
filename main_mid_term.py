# -*- coding: utf-8 -*-

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
#fpath = "/mnt/d/kt/project/yl/2023-HLJIEE-MicroMeteorologicalServices/ECMWF/C1D-grib/"
fpath='/share/Datasets/ECMWF/C1D-grib'
# 数据路径
latS = 42.0
latN = 55.0
lonL = 120.0
lonR = 135.5

variable_name = [
    "Convective available potential energy",
    "Total precipitation",
    #"10 metre wind gust in the last 3 hours",
    '10 metre wind gust in the last 6 hours'
]

# 如果出短临的 短临的 需要3小时的 和6小时的:短临一天
# 短期的 出三天， 需要6小时 不需要三小时

# 00 时的下午4点 出图，报告在出图之后
# 12 时的在凌晨4点 或者 5点 出图，报告出图之后
# 变量名，用于提取数据
variable_name_Zh = ["对流有效位能", "降水量", "最大风速"]
variabale_name_english_sort=['cp','pre','wins']

# 变量中文名用于生成图片中的标题
city_path = "./old/EC_D1D_PLOT/heilongjiang_shp/heilongjiang_city.shp"
province_path = "./old/EC_D1D_PLOT/heilongjiang_shp/"

manual_time = datetime.datetime(2023, 7, 29,5)  # 手动运行时指定的起报时刻（utc-8）
# 中期天气预报 24 小时间隔
forecast_step = 24
end = 220

#中期天气预报文件夹标记
forecast_type = "medium-term"  # Set the forecast type to 'short-term', 'medium-term', or 'long-term'
#output_prefix = "../output/"  # 输出图片路径前缀，命名

output_prefix='/share/data/pic_heilongjiang'   #输出的文件夹位置

#修改发布时间:

# output_prefix=os.path.join(output_prefix,manual_time.strftime('%Y%m%d')+"20")
# if not os.path.exists(output_prefix):
#     os.mkdir(output_prefix)
#     print("成功创建文件")

# %%

print("位能变量提取中")
cape_reader = GribDataReader(
    fpath, variable_name[0], manual_time=manual_time, forecast_step=forecast_step, end=end
)
cape, lats, lons = cape_reader.get_data()
forecast_start_time = cape_reader.base_time_str
forecast_end_time = cape_reader.forecast_time_str


#
# %%
tp_reader = GribDataReader(
    fpath, variable_name[1], manual_time=manual_time, forecast_step=forecast_step, end=end
)
tp,lats,lons = tp_reader.get_data()
forecast_start_time = tp_reader.base_time_str
forecast_end_time = tp_reader.forecast_time_str

#获取时间字符串,转换为 %m%d%H的形式
forecast_start_time_tofile=tp_reader.base_time_str_mdH
forecast_end_time_tofile=tp_reader.forecast_time_str_mdH



#%%
windspeed_reader = GribDataReader(
    fpath, variable_name[2], manual_time=manual_time, forecast_step=forecast_step, end=end
)
windspeed, _, _ = windspeed_reader.get_data()


# %%

# %%
for i in range(0, len(tp) - 1):
    levels = [0, 0.1, 1, 3, 10, 20, 50, 70]
    plotter = Plotter(  fpath,
        variable_name[0],
        ticks=None,
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[0]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[0].replace(" ", "_")}_{i}.png'
    filename=f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[0]}_forecast"+'.png'
    output_file = plotter.get_output_file_path(variable_name[0], i, output_prefix,filename)
    #print(filename.encode())
    subdirectories = plotter.create_subdirectories(output_prefix)  # 创建中期，短期，短临 文件夹
    
    #重新创建  
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
 
    plotter.plot_contour_map(
        lats,
        lons,
        cape[i],
        "对流有效位能/$J/kg$",
        levels=np.arange(200, 4001, 200),
        colormap=cmaps.WhBlGrYeRe,
        title=titles,
        output_file=output_file,
        tips="cmaps",
    )
    del titles, output_file
    levelsduanlin= [0, 0.1, 1, 3, 10, 20, 50, 70]
    levels=[0, 0.1, 10, 25, 50, 100, 250, 500]
    plotter = Plotter(
        fpath,
        variable_name[1],
        ticks=[0.1,10,25,50,100,250],
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )

    color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[1]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[1].replace(" ", "_")}_{i}.png'
    filename=f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[1]}_forecast"+'.png'
    output_file = plotter.get_output_file_path(variable_name[1], i, output_prefix,filename)
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
        draw_river=True
    )
    del titles, output_file

    #风速
    plotter = Plotter(
        fpath,
        variable_name[2],
        ticks=None,
        city_path=city_path,
        variables=variable_name,
        province_path=province_path,
        forecast_type=forecast_type,
    )
    titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[2]}预报图"
    # output_file = f'./output_file_rainfall_'+str(forecast_step)+'h_{i}.png'
    # output_file = f'{output_prefix}output_file_{forecast_type}_{str(forecast_step)}h_{variable_name[2].replace(" ", "_")}_{i}.png'
    filename=f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[2]}_forecast"+'.png'

    output_file = plotter.get_output_file_path(variable_name[2], i, output_prefix,filename)
    subdirectories = plotter.create_subdirectories(output_prefix)
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
    plotter.plot_contour_map(
        lats,
        lons,
        windspeed[i],
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
#levels=np.arange(0,35,2)
