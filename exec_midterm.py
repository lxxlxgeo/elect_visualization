# -*- coding: utf-8 -*-

from src.data_reader import GribDataReader
from src.data_plotter import Plotter
from src.configure import *
import os
import cmaps



def exec_term(fpath,variable_name,manual_time,forecast_step,end,forecast_type,color_bar_config,output_prefix,forecast_type_tips,variabale_name_folder):

    #读取位能变量
    print("读取位能变量.....")
    cape_reader = GribDataReader (
        fpath, variable_name[0],forecast_type,forecast_type_tips, manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    cape, lats, lons = cape_reader.get_data ()

    #读取时间，供出图使用
    forecast_start_time = cape_reader.base_time_str
    forecast_end_time = cape_reader.forecast_time_str
    forecast_start_time_tofile =cape_reader.base_time_str_mdH
    forecast_end_time_tofile = cape_reader.forecast_time_str_mdH

    #第一报时间字符串
    forecast_path_timestr=cape_reader.base_time_str_YmdH
    print(cape_reader.base_time_str_YmdH)

    print('读取降水变量')
    #获取降水变量
    tp_reader = GribDataReader (
        fpath, variable_name[1],forecast_type,forecast_type_tips,manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    tp, _, _ = tp_reader.get_data ()
    #获取风速变量
    print('读取风速变量')
    windspeed_reader = GribDataReader (
        fpath, variable_name[2],forecast_type,forecast_type_tips, manual_time=manual_time, forecast_step=forecast_step, end=end
    )
    windspeed, _, _ = windspeed_reader.get_data ()
    #print(len(tp),'tp长度')

    print("执行渲染程序,可视化中........")
    for i in range (0, len (tp)):
        #p=20
        plotter = Plotter (fpath,
                           variable_name[0],
                           ticks=None,
                           forecast_path_str=forecast_path_timestr,
                           variables=variabale_name_folder,
                           forecast_type=forecast_type,
                           )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[0]}预报图"
        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[0]}_forecast" + '.png'
        output_file = plotter.get_output_file_path (variabale_name_english_sort[0], i, output_prefix, filename)

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
            variables=variabale_name_folder,
            forecast_type=forecast_type,
        )

        color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[1]}预报图"

        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[1]}_forecast" + '.png'

        output_file = plotter.get_output_file_path (variabale_name_english_sort[1], i, output_prefix, filename)
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
        #print(output_file,' 输出位置在这里')
        del titles, output_file

        # 风速
        plotter = Plotter (
            fpath,
            variable_name[2],
            ticks=None,
            forecast_path_str=forecast_path_timestr,
            variables=variabale_name_folder,
            forecast_type=forecast_type,
        )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[2]}预报图"

        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[2]}_forecast" + '.png'

        output_file = plotter.get_output_file_path (variabale_name_english_sort[2], i, output_prefix, filename)
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
    print('执行完毕')

def convert_exec_run(exec_time,forecast_type,forecast_type_tips):
    mid_color_config, short_term_color_config = generate_color_conf ()
    hour=exec_time.hour
    if hour==11:
        step_offset=0
    elif hour==5:
        step_offset=12
    if forecast_type_tips=='imminent':
        forecast_step=3
        end=25+step_offset+forecast_step
        color_conf=short_term_color_config
        tvariable_name=imminent_variable_name

    else:
        if forecast_type=='medium-term':
            forecast_step=24
            end=168+step_offset+forecast_step
            color_conf=mid_color_config
            tvariable_name=mid_variable_name
        elif forecast_type=='short-term':
            forecast_step=24
            end=72+step_offset+forecast_step
            color_conf=mid_color_config
            tvariable_name=mid_variable_name
        elif forecast_type=='imminent':
            forecast_step=24
            end=24+step_offset+forecast_step
            color_conf=mid_color_config
            tvariable_name=mid_variable_name
        else:
            print("变量引用错误")

    return forecast_step,end,color_conf,tvariable_name






if __name__=='__main__':

    #执行时间，configure.py文件里，根据当前时间返回运行时间
    #exec_time=convert_BTJ()
    exec_time=datetime.datetime(2023,7,28,11)
    #exec_time=convert_BTJ()

    #执行顺序
    #forecast_type 对应的关系： imminent 为短临预报，short-term 为短期预报，medium-term为中期预报
    #forecast_type_tips 对应关系: imminent 为输出短临间隔3小时预报,None 为不执行这一项

    forecast_type_imminent= "imminent"
    forecast_type_tips_imminent="imminent"

    forecast_type_short='short-term'
    forecast_type_medium='medium-term'


    #转换短临预报3小时
    forecast_step_imminent3,end_imminent,color_conf_imminent,tvariable_name_imminent=\
        convert_exec_run(exec_time,forecast_type_imminent,forecast_type_tips_imminent)
    #转换短临预报24小时
    forecast_step_imminent24,end_imminent,color_conf,tvariable_name=convert_exec_run(exec_time,forecast_type_imminent,None)

    #转换短期预报3天
    forecast_step,end_short,color_conf,tvariable_name=convert_exec_run(exec_time,forecast_type_short,None)

    #转换中期预报7天
    forecast_step,end_medium,color_conf,tvariable_name=convert_exec_run(exec_time,forecast_type_medium,None)




    #执行短临预报3小时间隔
    exec_term(fpath,tvariable_name_imminent,exec_time,forecast_step_imminent3,end_imminent,forecast_type_imminent,color_conf_imminent,output_prefix,forecast_type_tips_imminent,variabale_name_english_sort)

    #执行短临预报24小时间隔
    exec_term(fpath,tvariable_name,exec_time,forecast_step_imminent24,end_imminent,forecast_type_imminent,color_conf,output_prefix,None,variabale_name_english_sort)

    #执行短期预报3天内
    exec_term(fpath,tvariable_name,exec_time,forecast_step,end_short,forecast_type_short,color_conf,output_prefix,None,variabale_name_english_sort)

    #执行中期预报7天内

    exec_term(fpath,tvariable_name,exec_time,forecast_step,end_medium,forecast_type_medium,color_conf,output_prefix,None,variabale_name_english_sort)






