# -*- coding: utf-8 -*-
# %%
from src.data_reader import GribDataReader
from src.data_plotter import Plotter
from src.configure import *
import os
import cmaps
#from message.seed_message import exec_seed_message


# %%
def exec_term(fpath, variable_name, manual_time, forecast_step, end, forecast_type, color_bar_config, output_prefix,
              forecast_type_tips, variabale_name_folder):
    # 读取位能变量
    print("读取位能变量.....")
    cape_reader = GribDataReader(
        fpath, variable_name[0], forecast_type, forecast_type_tips, manual_time=manual_time,
        forecast_step=forecast_step, end=end
    )
    cape, lats, lons = cape_reader.get_data()

    # 读取时间，供出图使用
    forecast_start_time = cape_reader.base_time_str
    forecast_end_time = cape_reader.forecast_time_str
    forecast_start_time_tofile = cape_reader.base_time_str_mdH
    forecast_end_time_tofile = cape_reader.forecast_time_str_mdH

    # 第一报时间字符串
    forecast_path_timestr = cape_reader.base_time_str_YmdH
    print(cape_reader.base_time_str_YmdH)

    print('读取降水变量')
    # 获取降水变量
    tp_reader = GribDataReader(
        fpath, variable_name[1], forecast_type, forecast_type_tips, manual_time=manual_time,
        forecast_step=forecast_step, end=end
    )
    tp, _, _ = tp_reader.get_data()
    # 获取风速变量
    print('读取风速变量')
    windspeed_reader = GribDataReader(
        fpath, variable_name[2], forecast_type, forecast_type_tips, manual_time=manual_time,
        forecast_step=forecast_step, end=end
    )
    windspeed, _, _ = windspeed_reader.get_data()
    # print(len(tp),'tp长度')

    print("执行渲染程序,可视化中........")
    for i in range(0, len(tp)):
        # p=20
        plotter = Plotter(fpath,
                          variable_name[0],
                          ticks=None,
                          forecast_path_str=forecast_path_timestr,
                          variables=variabale_name_folder,
                          forecast_type=forecast_type,
                          )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[0]}预报图"
        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[0]}_forecast" + '.png'
        tifname=f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[0]}_forecast" + '.tif'
        output_file = plotter.get_output_file_path(variabale_name_english_sort[0], i, output_prefix, filename)
        output_file_cape = plotter.get_output_file_path(variabale_name_english_sort[0], i, output_prefix, tifname)





        subdirectories = plotter.create_subdirectories(output_prefix)  # 创建中期，短期，短临 文件夹

        # 重新创建
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)

        plotter.plot_contour_map(
            lats,
            lons,
            cape[i],
            "对流有效位能/$J/kg$",
            levels=color_bar_config['cape_level'],
            colormap=cmaps.WhBlGrYeRe,
            title=titles,
            output_file=output_file,
            tips="cmaps"
        )
        del titles, output_file

        # 降水量出图

        plotter = Plotter(
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

        output_file = plotter.get_output_file_path(variabale_name_english_sort[1], i, output_prefix, filename)
        subdirectories = plotter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        plotter.plot_contour_map(
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
        # print(output_file,' 输出位置在这里')
        del titles, output_file

        # 风速
        plotter = Plotter(
            fpath,
            variable_name[2],
            ticks=None,
            forecast_path_str=forecast_path_timestr,
            variables=variabale_name_folder,
            forecast_type=forecast_type,
        )
        titles = f"{forecast_start_time[i]}-{forecast_end_time[i]}黑龙江省{variable_name_Zh[2]}预报图"

        filename = f"{forecast_start_time_tofile[i]}_{forecast_end_time_tofile[i]}_heilongjiang_{variabale_name_english_sort[2]}_forecast" + '.png'

        output_file = plotter.get_output_file_path(variabale_name_english_sort[2], i, output_prefix, filename)
        subdirectories = plotter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        plotter.plot_contour_map(
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


# %%

'''
            if hour==11:
                #北京时间11时运行，UTC为03时
                return list(range(15,self.end,self.forecast_step))
            elif hour==5:
                return list(range(9,self.end,self.forecast_step))
            elif hour==17:
                return  list(range(9,self.end,self.forecast_step))
            elif hour==23:
                return  list(range(15,self.forecast_step,self.forecast_step))
'''


def convert_exec_run(exec_time, forecast_type, forecast_type_tips):
    mid_color_config, short_term_color_config = generate_color_conf()
    hour = exec_time.hour

    if forecast_type_tips == 'imminent':
        if hour == 11:
            step_offset = 15
        elif hour == 5:
            step_offset = 9
        elif hour == 17:
            step_offset = 9
        elif hour == 23:
            step_offset = 15
        elif hour == 2:
            step_offset = 18
        elif hour == 20:
            step_offset = 12
        elif hour == 8:
            step_offset = 12
        elif hour == 14:
            step_offset = 18
        forecast_step = 3
        print(step_offset)
        end = 24 + step_offset + forecast_step
        color_conf = short_term_color_config
        tvariable_name = imminent_variable_name
        return forecast_step, end, color_conf, tvariable_name

    else:
        if hour == 11 or hour == 23:
            step_offset = 0
        elif hour == 5 or hour == 17:
            step_offset = 12
        elif hour == 20 or hour == 8:
            step_offset = 12
        elif hour == 2 or hour == 14:
            step_offset = 18
        if forecast_type == 'medium-term':
            forecast_step = 24
            end = 168 + step_offset + forecast_step
            color_conf = mid_color_config
            tvariable_name = mid_variable_name
        elif forecast_type == 'short-term':
            forecast_step = 24
            end = 72 + step_offset + forecast_step
            color_conf = mid_color_config
            tvariable_name = mid_variable_name
        elif forecast_type == 'imminent':
            forecast_step = 24
            end = 24 + step_offset
            color_conf = mid_color_config
            tvariable_name = mid_variable_name
        else:
            print("变量引用错误")
        return forecast_step, end, color_conf, tvariable_name


# %%
if __name__ == '__main__':

    # 执行时间，configure.py文件里，根据当前时间返回运行时间
    # exec_time=convert_BTJ()
    # exec_time=datetime.datetime(2023,7,31,11)
    # 启动时间为 凌晨4点 或者16点
    # exec_time=convert_BTJ_imminent11()
    # print(exec_time)
    # 短期或中期启动时间

    start_process_time = datetime.datetime.now()
    print("程序开始于 {}".format(start_process_time))
    exec_time = convert_BTJ()

    # 短临启动时间 第一次起报05时
    exec_imminent_05f = convert_BTJ_imminent_05f()
    # 短临启动时间 第一次起报11时
    exec_imminent_11f = convert_BTJ_imminent_11f()
    #

    # 短临 20-20时的第一次运行  ,
    exec_imminent_20f = convert_BTJ_imminent_20f()

    # 短临 02-02时的第二次运行

    exec_imminent_02f = convert_BTJ_imminent_02f()

    # 启动时间 17,23
    # exec_time_imminent1=convert_BTJ_imminent()

    # 启动时间 5,11
    # exec_time_imminent2=convert_BTJ()

    # 执行顺序
    # forecast_type 对应的关系： imminent 为短临预报，short-term 为短期预报，medium-term为中期预报
    # forecast_type_tips 对应关系: imminent 为输出短临间隔3小时预报,None 为不执行这一项

    # 短临标识
    forecast_type_imminent = "imminent"
    # 短临辅助标识
    forecast_type_tips_imminent = "imminent"

    # 短期标识
    forecast_type_short = 'short-term'
    # 中期标识
    forecast_type_medium = 'medium-term'

    '''
    短临预报转化,稍微有点复杂
    短临预报状态转换
    '''
    # 转换短临预报3小时，状态1为05时，状态2为11，状态1为17时，状态2 为23
    forecast_step_imminent3_stuts1, end_imminent_stuts1, color_conf_imminent, tvariable_name_imminent = \
        convert_exec_run(exec_imminent_05f, forecast_type_imminent, forecast_type_tips_imminent)
    # print(end_imminent_stuts1)
    # 转换短临预报3小时，状态2
    forecast_step_imminent3_stuts2, end_imminent_stuts2, color_conf_imminent, tvariable_name_imminent = \
        convert_exec_run(exec_imminent_11f, forecast_type_imminent, forecast_type_tips_imminent)
    # print(end_imminent_stuts2)

    # 转换短临预报24小时，状态1
    forecast_step_imminent24_stuts1, end_stuts1, color_conf, tvariable_name = \
        convert_exec_run(exec_imminent_05f, forecast_type_imminent, None)

    # #转换短临预报24小时，状态2
    forecast_step_imminent24_stuts2, end_stuts2, color_conf, tvariable_name = \
        convert_exec_run(exec_imminent_11f, forecast_type_imminent, None)

    # 转换短临预报3小时，状态3
    forecast_step_imminent3_stuts3, end_imminent_stuts3, color_conf_imminent, tvariable_name_imminent = \
        convert_exec_run(exec_imminent_02f, forecast_type_imminent, forecast_type_tips_imminent)

    # 转换短临预报3小时，状态4
    forecast_step_imminent3_stuts4, end_imminent_stuts4, color_conf_imminent, tvariable_name_imminent = \
        convert_exec_run(exec_imminent_20f, forecast_type_imminent, forecast_type_tips_imminent)

    # forecast_step_02_20_14_18,end_imminent_02_20_14_18,color_conf,tvariable_name=convert_exec_run(exec_imminent_02f,forecast_type_imminent,None)

    # 短临24小时，状态3
    forecast_step_imminent24_stuts3, end_stuts3, color_conf, tvariable_name = \
        convert_exec_run(exec_imminent_02f, forecast_type_imminent, None)
    # 短临24小时，状态4

    forecast_step_imminent24_stuts4, end_stuts4, color_conf, tvariable_name = \
        convert_exec_run(exec_imminent_20f, forecast_type_imminent, None)

    # 转换短临预报24小时
    forecast_step_imminent24, end_imminent, color_conf, tvariable_name = convert_exec_run(exec_time,
                                                                                          forecast_type_imminent, None)

    # 转换短期预报3天
    forecast_step, end_short, color_conf, tvariable_name = convert_exec_run(exec_time, forecast_type_short, None)

    # 转换中期预报7天
    forecast_step, end_medium, color_conf, tvariable_name = convert_exec_run(exec_time, forecast_type_medium, None)

    # exec_term(fpath,tvariable_name_imminent,datetime.datetime(2023,8,1,11),forecast_step_imminent3_stuts1,end_imminent_stuts1,forecast_type_imminent)
    # print(exec_time_imminent1)

    # 执行短临预报3小时间隔,状态1

    '''
    定时2
    '''
    # #短临预报状态1开始

    try:
        exec_term(fpath, tvariable_name_imminent, exec_imminent_05f, forecast_step_imminent3_stuts1,
                  end_imminent_stuts1, forecast_type_imminent,
                  color_conf_imminent, output_prefix, forecast_type_tips_imminent, variabale_name_english_sort)

        # #print(exec_time_imminent1)
        # # #执行短临预报3小时间隔，状态2

        # '''
        # 定时1
        # '''
        # #短临预报状态2 开始
        exec_term(fpath, tvariable_name_imminent, exec_imminent_11f, forecast_step_imminent3_stuts2,
                  end_imminent_stuts2, forecast_type_imminent,
                  color_conf_imminent, output_prefix, forecast_type_tips_imminent, variabale_name_english_sort)
        # #print(exec_imminent_11f)

        # 短临3小时 状态3 状态3 对应02f
        exec_term(fpath, tvariable_name_imminent, exec_imminent_02f, forecast_step_imminent3_stuts3,
                  end_imminent_stuts3, forecast_type_imminent,
                  color_conf_imminent, output_prefix, forecast_type_tips_imminent, variabale_name_english_sort)

        # 短临预报3小时 状态4 状态4 对应 20f
        exec_term(fpath, tvariable_name_imminent, exec_imminent_20f, forecast_step_imminent3_stuts4,
                  end_imminent_stuts4, forecast_type_imminent,
                  color_conf_imminent, output_prefix, forecast_type_tips_imminent, variabale_name_english_sort)

        ########################################
        # # #执行短临预报24小时间隔，状态1
        exec_term(fpath, tvariable_name_imminent, exec_imminent_05f, forecast_step_imminent24_stuts1,
                  end_imminent_stuts1,
                  forecast_type_imminent, color_conf, output_prefix, None, variabale_name_english_sort)

        # #执行短临预报24小时间隔，状态2
        exec_term(fpath, tvariable_name_imminent, exec_imminent_11f, forecast_step_imminent24_stuts2,
                  end_imminent_stuts2, forecast_type_imminent, color_conf, output_prefix, None,
                  variabale_name_english_sort)
        ##############################################

        exec_term(fpath, tvariable_name_imminent, exec_imminent_02f, forecast_step_imminent24_stuts3,
                  end_imminent_stuts3, forecast_type_imminent, color_conf, output_prefix, None,
                  variabale_name_english_sort)

        exec_term(fpath, tvariable_name_imminent, exec_imminent_20f, forecast_step_imminent24_stuts4,
                  end_imminent_stuts4, forecast_type_imminent, color_conf, output_prefix, None,
                  variabale_name_english_sort)

        # exec_term(fpath,tvariable_name_imminent,exec)

        # 执行短期预报3天内
        exec_term(fpath, tvariable_name, exec_time, forecast_step, end_short, forecast_type_short, color_conf,
                  output_prefix, None, variabale_name_english_sort)

        # 执行中期预报7天内

        exec_term(fpath, tvariable_name, exec_time, forecast_step, end_medium, forecast_type_medium, color_conf,
                  output_prefix, None, variabale_name_english_sort)
    except Exception as e:
        print("出错,错误信息")
        print(e)
        #exec_seed_message()
    end_time_now = datetime.datetime.now()
    print("程序结束于: {}".format(end_time_now))

    print("总计耗时:{}".format(end_time_now - start_process_time))

# %%
