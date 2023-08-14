# -*- coding: utf-8 -*-
"""
Created on 2023/8/14 5:44

@author: lxce
"""
#%%
from RLDAS_self.cldas_plot import Plotter
from RLDAS_self.RLdas_Read import RlDas_Reader
import datetime
from un_config.rldas_configl import generate_color_conf,map_extent,output_prefix
import os


# %%
if __name__=='__main__':
    #%%
    mid_term,imm_term=generate_color_conf()
    start_time=datetime.datetime(2023,8,14,8)
    end_time=datetime.datetime(2023,8,17,8)
    step=24
    #读取降水变量
    CLDAS_Data_Reader=RlDas_Reader(start_time,end_time,step)
    pre_data_list=CLDAS_Data_Reader.get_data('pre')
    lon,lat,proj=CLDAS_Data_Reader.__get__init_field_info__()
    data_extent=CLDAS_Data_Reader.data_extent
    #wind_data_list=CLDAS_Data_Reader.get_data('WIN','WIND','max')

    start_time_str=start_time.strftime('%Y%m%d%H')

    #%%

    #绘制降水
    for item in pre_data_list:
        data=item['data']
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
            data_extent=data_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type='fourdayd2'
        )
        color=("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
        titles=f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报"
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
            draw_river=True
        )
        del titles,out_file