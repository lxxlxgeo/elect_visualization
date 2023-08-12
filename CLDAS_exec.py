# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 6:10

@author: lxce
"""
import datetime

from cldas.data_reader import Cldas_Reader
from cldas.data_plot import Plotter
from un_config.cldas_config import generate_color_conf,output_prefix
import cmaps
import os
def exec_main(start_time:datetime.datetime,end_time,step):

    mid_term,imm_term=generate_color_conf()

    #读取降水变量
    CLDAS_Data_Reader=Cldas_Reader(start_time,end_time,step)
    pre_data_list=CLDAS_Data_Reader.get_data('PRE','PRCP','sum')
    wind_data_list=CLDAS_Data_Reader.get_data('WIN','WIND','max')

    start_time_str=start_time.strftime('%Y%m%d%H')


    #绘制降水
    for item in pre_data_list:
        data=item['data']
        lon=item['lon']
        lat=item['lat']
        forecast_start_time=item['forecast_start_time']
        forecast_end_time=item['forecast_end_time']
        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')

        #降水变量绘图
        pre_ploter=Plotter(
            variable_name='pre',
            variables=['pre','wins'],
            ticks=mid_term['pre_ticks'],
            forecast_path_str=start_time_str,
            forecast_type='scene'
        )
        color=("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
        titles=f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量实况图"
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_scene" + '.png'
        out_file=pre_ploter.get_output_file_path('pre',1,output_prefix,filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            data,
            "降水量/$mm$",
            levels=mid_term['pre_level'],
            colormap=color,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=False
        )
        del titles,out_file

    for item in wind_data_list:
        data=item['data']
        lon=item['lon']
        lat=item['lat']
        forecast_start_time=item['forecast_start_time']
        forecast_end_time=item['forecast_end_time']
        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        #风速
        wins_ploter=Plotter(
            variable_name='wins',
            variables=['pre', 'wins'],
            ticks=None,
            forecast_path_str=start_time_str,
            forecast_type='scene'
        )
        titles=f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省最大风速实况图"
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_wins_scene" + '.png'
        out_file=wins_ploter.get_output_file_path('wins',1,output_prefix,filename)
        subdirectories = wins_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)

        wins_ploter.plot_contour_map(
            lat,
            lon,
            data,
            "风速/$mm$",
            levels=mid_term['wins_level'],
            colormap=cmaps.wind_17lev,
            title=titles,
            output_file=out_file,
            tips="cmaps",
            draw_river=False
        )
        del titles,out_file



if __name__=='__main__':
    exec_main(datetime.datetime(2023,8,10,8),datetime.datetime(2023,8,11,8),step=24)
