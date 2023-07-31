# -*- coding: utf-8 -*-

from src.data_reader import GribDataReader
from src.data_plotter import Plotter
from src.configure import *
import os
import cmaps



def exec_mid_term(fpath,variable_name,manual_time,forecast_step,end,forecast_type,color_bar_config,output_prefix):

    #读取位能变量
    cape_reader = GribDataReader (
        fpath, variable_name[0],forecast_type, manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    cape, lats, lons = cape_reader.get_data ()

    #读取时间，供出图使用
    forecast_start_time = cape_reader.base_time_str
    forecast_end_time = cape_reader.forecast_time_str
    forecast_start_time_tofile =cape_reader.base_time_str_mdH
    forecast_end_time_tofile = cape_reader.forecast_time_str_mdH

    #第一报时间字符串
    forecast_path_timestr=cape_reader.forecast_time_str_YmdH[0]


    #获取降水变量
    tp_reader = GribDataReader (
        fpath, variable_name[1],forecast_type,manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    tp, _, _ = tp_reader.get_data ()
    #获取风速变量
    windspeed_reader = GribDataReader (
        fpath, variable_name[2],forecast_type, manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    windspeed, _, _ = windspeed_reader.get_data ()

    for i in range (0, len (tp) - 1):

        plotter = Plotter (fpath,
                           variable_name[0],
                           ticks=None,
                           forecast_path_str=forecast_path_timestr,
                           variables=variable_name,
                           forecast_type=forecast_type,
                           )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[0]}预报图"
        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[0]}_forecast" + '.png'
        output_file = plotter.get_output_file_path (variable_name[0], i, output_prefix, filename)

        subdirectories = plotter.create_subdirectories (output_prefix)  # 创建中期，短期，短临 文件夹

        # 重新创建
        for subdirectory in subdirectories.values ():
            os.makedirs (subdirectory, exist_ok=True)

        plotter.plot_contour_map (
            lats,
            lons,
            cape[i],
            "对流有效位能/$J/kg$",
            levels=color_bar_config['cape_level'],
            colormap=cmaps.WhBlGrYeRe,
            title=titles,
            output_file=output_file,
            tips="cmaps",
        )
        del titles, output_file

        # 降水量出图

        plotter = Plotter (
            fpath,
            variable_name[1],
            ticks=color_bar_config['pre_ticks'],
            forecast_path_str=forecast_path_timestr,
            variables=variable_name,
            forecast_type=forecast_type,
        )

        color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[1]}预报图"

        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[1]}_forecast" + '.png'

        output_file = plotter.get_output_file_path (variable_name[1], i, output_prefix, filename)
        subdirectories = plotter.create_subdirectories (output_prefix)
        for subdirectory in subdirectories.values ():
            os.makedirs (subdirectory, exist_ok=True)
        plotter.plot_contour_map (
            lats,
            lons,
            tp[i],
            "降水量/$mm$",
            levels=color_bar_config['pre_level'],
            colormap=color,
            title=titles,
            output_file=output_file,
            tips="colors",
            draw_river=True
        )
        del titles, output_file

        # 风速
        plotter = Plotter (
            fpath,
            variable_name[2],
            ticks=None,
            forecast_path_str=forecast_path_timestr,
            variables=variable_name,
            forecast_type=forecast_type,
        )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[2]}预报图"

        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[2]}_forecast" + '.png'

        output_file = plotter.get_output_file_path (variable_name[2], i, output_prefix, filename)
        subdirectories = plotter.create_subdirectories (output_prefix)
        for subdirectory in subdirectories.values ():
            os.makedirs (subdirectory, exist_ok=True)
        plotter.plot_contour_map (
            lats,
            lons,
            windspeed[i],
            "风速/$m/s$",
            levels=color_bar_config['wins_level'],
            colormap=cmaps.wind_17lev,
            #  colormap=color,
            title=titles,
            output_file=output_file,
            tips="cmaps",
        )
        del titles, output_file

if __name__=='__main__':

    #执行时间，configure.py文件里，根据当前时间返回运行时间
    #exec_time=convert_BTJ()
    exec_time=datetime.datetime(2023,7,28,17)
    forecast_step=25
    end=220
    forecast_type = "medium-term"
    mid_color_config,short_term_color_config=generate_color_conf()
    output_prefix=r'G:/js_elect/ECFile'
    exec_mid_term(fpath,mid_variable_name,exec_time,3,25,"imminent",short_term_color_config,output_prefix)







